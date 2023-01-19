#!/usr/bin/env python
import os
from flask import request, Response, render_template, Flask
import numpy as np
import io
import pandas as pd
import pickle
import bz2
import geopandas as gpd
from haversine import haversine_vector, Unit
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Circle
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
sns.set()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', ref_key='')


@app.route('/<city_link>')
def process_city(city_link=None):
    ref_key, continent, exclusion_radius = (city_link.replace("_","/").replace("-"," ")).split('&')
    exclusion_radius = float(exclusion_radius)
    if continent=='All': continent=None
    #Make climate comparison plot
    filter_text = ''
    if not (continent is None): filter_text+=' in '+continent
    if exclusion_radius>0: filter_text+=', excluding cities within %d km'%(int(exclusion_radius))
    plot1_data, best_matches = climate_similarity_map(ref_key, limits=continent, exclusion_radius=exclusion_radius )

    #Add reference to plot in buffer to the html
    return render_template('index.html', ref_key=ref_key, plot1_data=plot1_data, filter_text=filter_text, best_matches=best_matches)


def get_geo_distances(df,ref_key):
    #Get the geographical (Haversine) distance for all cities relative to the reference point
    ref_ind = np.argmax(df.index==ref_key)
    coords = np.array(df[['Latitude', 'Longitude']])
    ref_coords = np.tile( [df['Latitude'][ref_ind], df['Longitude'][ref_ind]], (len(df.index),1) )
    return haversine_vector( coords, ref_coords)
    
def city_coords(df, ref_key, longitude_first=True):
    ref_ind = np.argmax(df.index==ref_key)
    if longitude_first:
        return np.array([df['Longitude'][ref_ind], df['Latitude'][ref_ind]])
    else:
        return np.array([df['Latitude'][ref_ind], df['Longitude'][ref_ind]])
        
def climate_similarity_map(ref_key, N_elem_per_chunk=500, dist_scale=0.5,  palette='inferno', symbol_scale=2, limits=None, exclusion_radius=0):
    #Load dataframe
    df = pd.read_csv('db/cities.csv', dtype={ 'Key': 'unicode', 'City': 'unicode', 'Longitude': float, 'Latitude': float})
    df.set_index('Key',inplace=True)
    #Find reference city
    ref_ind = np.argmax(df.index==ref_key)
    chunk_ind = int(ref_ind/N_elem_per_chunk)
    ref_ind_in_chunk = ref_ind - chunk_ind*N_elem_per_chunk
    dist_mtx = pickle_load("db/city_climate_dist_mtx_red_%d.p"%(chunk_ind), use_bz2=True)
    distances = dist_mtx[ref_ind_in_chunk,:]
    #Find best matching cities after filtering
    geo_distance = get_geo_distances(df,ref_key)
    filter = (geo_distance>exclusion_radius)
    if isinstance(limits, str):
        filter = filter & (np.array(df['Region']==limits))
    sortind = np.argsort(distances[filter])
    sorted_keys = (df.index[filter])[sortind]
    best_matches = []
    for i in range(min(5,len(sorted_keys))):
        best_matches.append( [sorted_keys[i],distances[filter][sortind][i] ] )
    #Generate the figure **without using pyplot**.
    fig = Figure(figsize=(20, 10), dpi=100)
    ax = fig.subplots()
    worldmap = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    worldmap.plot(color="lightgrey", ax=ax)
    dist_norm = np.clip( distances / dist_scale, 0, 1)[filter]
    sns.scatterplot(data=df[filter],x='Longitude',y='Latitude',hue=dist_norm, s=symbol_scale*(2+4/(dist_norm+0.02)), palette=palette, ax=ax )
    #Mark refernce city
    ref_coord = city_coords(df,ref_key)
    ax.scatter(ref_coord[0], ref_coord[1], c='b', s=200, marker='*')
    #Mark best matches
    for match in best_matches:
        coord = city_coords(df, match[0])
        ax.scatter(coord[0], coord[1], c='g', s=200, marker='x')
    ax.legend([],[], frameon=False)
    #Set plot limits
    if not (limits is None):
        if isinstance(limits, str):
            if limits=='North America':
                xlim = [-130,-60]; ylim = [20,55]
            elif limits=='US-East': 
                xlim = [-100,-50]; ylim = [25,55]
            elif limits=='US-West': 
                xlim = [-130,-100]; ylim = [20,55]
            elif limits=='Europe': 
                xlim = [-10,40]; ylim = [35,71]
            elif limits=='Europe+Mediterranean': 
                xlim = [-10,50]; ylim = [25,71]
            elif limits=='Asia': 
                xlim = [40,150]; ylim = [5,71] 
            elif limits=='South-East Asia': 
                xlim = [60,150]; ylim = [-10,40] 
            elif limits=='Antarctica': 
                xlim = [-180,180]; ylim = [-90,-50]
            elif limits=='Africa': 
                xlim = [-20,55]; ylim = [-35,40]
            elif limits=='Caribbean': 
                xlim = [-90,-60]; ylim = [10,30]
            if limits=='Central America':
                xlim = [-110,-65]; ylim = [0,25]
            if limits=='Middle East':
                xlim = [30,65]; ylim = [10,45]
            if limits=='South America':
                xlim = [-90,-35]; ylim = [-60,20]
            if limits=='Oceania':
                xlim = [110,180]; ylim = [-50,0] 
        else:
            xlim = limits[0]; ylim = limits[1];
        ax.set_xlim(xlim[0],xlim[1]); ax.set_ylim(ylim[0],ylim[1])
    fig.set_tight_layout(True)
    # Save it to a temporary buffer.
    buf = io.BytesIO()
    fig.savefig(buf, format="png",bbox_inches='tight')
    #Get address for image in buffer
    plot1_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return plot1_data, best_matches

def pickle_load(fname, use_bz2=False):
    if use_bz2:
        with bz2.BZ2File(fname, 'rb') as pickle_in:
            var = pickle.load(pickle_in, encoding='bytes')
    else:
        with open(fname,'rb') as pickle_in:
            var = pickle.load(pickle_in)
    return var



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

