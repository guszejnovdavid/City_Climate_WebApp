#!/usr/bin/env python
import os
from flask import request, Response, render_template, Flask
import numpy as np
import io
import pandas as pd
import pickle
import bz2
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
sns.set()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', ref_key='')


@app.route('/<ref_key>')
def process_city(ref_key=None):
    ref_key = ref_key.replace("_","/").replace("-"," ")
    
    #Make climate comparison plot
    plot1_data = climate_similarity_map(ref_key)

    #Add reference to plot in buffer to the html
    return render_template('index.html', ref_key=ref_key, plot1_data=plot1_data)



def climate_similarity_map(ref_key, N_elem_per_chunk=500, dist_scale=0.5,  palette='inferno', symbol_scale=2):


    df = pd.read_csv('db/cities.csv', dtype={ 'Key': 'unicode', 'City': 'unicode', 'Longitude': float, 'Latitude': float})
    df.set_index('Key',inplace=True)
    
    
    ref_ind = np.argmax(df.index==ref_key)
    chunk_ind = int(ref_ind/N_elem_per_chunk)
    ref_ind_in_chunk = ref_ind - chunk_ind*N_elem_per_chunk
    dist_mtx = pickle_load("db/city_climate_dist_mtx_red_%d.p"%(chunk_ind), use_bz2=True)
    distances = dist_mtx[ref_ind_in_chunk,:]
    
    

    # Generate the figure **without using pyplot**.
    fig = Figure(figsize=(20, 10), dpi=100)
    ax = fig.subplots()
    worldmap = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    worldmap.plot(color="lightgrey", ax=ax)
    dist_norm = np.clip( distances / dist_scale, 0, 1)
    sns.scatterplot(data=df,x='Longitude',y='Latitude',hue=dist_norm, s=symbol_scale*(2+4/(dist_norm+0.02)), palette=palette, ax=ax )
    ax.legend([],[], frameon=False)
    
    
    
    # x = np.arange(-50,50)
    # ax.scatter(x,x)
    # ax.text(0.0,0.0,'%s %d %d %d %g %d %d'%(ref_key, ref_ind, chunk_ind, ref_ind_in_chunk, distances[0],N_elem_per_chunk, dist_mtx.shape[0]  ))
    
    
    
    
    
    
    
    
    # Save it to a temporary buffer.
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    #Get address for image in buffer
    plot1_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return plot1_data






# def climate_similarity_map(ref_key, distances, df, symbol_scale=2, palette='inferno', limits=None, scale=None, fname=None):
    # if scale is None:
        # dist_scale = 0.5
    # elif isinstance(scale, str):
        # dist_scale = 0.5 * distances[np.argmax(df.index==ref_key),np.argmax(df.index==scale)]
    # else:
        # dist_scale = scale
    # dist_norm = np.clip( distances[np.argmax(df.index==ref_key),:] / dist_scale, 0, 1)
    # fig, ax = plt.subplots(figsize=(20, 10),dpi=250)
    # worldmap.plot(color="lightgrey", ax=ax)
    # sns.scatterplot(data=df,x='Longitude',y='Latitude',hue=dist_norm, s=symbol_scale*(2+4/(dist_norm+0.02)), palette=palette ); 
    # plt.legend([],[], frameon=False);
    # if not (limits is None):
        # if isinstance(limits, str):
            # if limits=='US':
                # xlim = [-130,-60]; ylim = [20,55]
            # elif limits=='US_East': 
                # xlim = [-100,-50]; ylim = [25,55]
            # elif limits=='US_West': 
                # xlim = [-130,-100]; ylim = [20,55]
            # elif limits=='Europe': 
                # xlim = [-10,50]; ylim = [25,70]
            # elif limits=='Australia': 
                # xlim = [110,180]; ylim = [-50,0] 
            # elif limits=='Asia': 
                # xlim = [40,150]; ylim = [5,65] 
        # else:
            # xlim = limits[0]; ylim = limits[1];
        # plt.xlim(xlim); plt.ylim(ylim)
    # if not(fname is None): plt.savefig(fname, dpi=200, bbox_inches='tight')
    # plt.show()



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

