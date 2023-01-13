#!/usr/bin/env python
import os
from flask import request, Response, render_template, Flask
import numpy as np
import io
import pandas as pd
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
def make_plots(ref_key=None):
    ref_key = ref_key.replace("_","/").replace("-"," ")
    
    
    # Generate the figure **without using pyplot**.
    fig = Figure(figsize=(20, 10), dpi=100)
    ax = fig.subplots()
    worldmap = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    worldmap.plot(color="lightgrey", ax=ax)
    x = np.arange(-50,50)
    ax.scatter(x,x)
    # Save it to a temporary buffer.
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    plot1_data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return render_template('index.html', ref_key=ref_key, plot1_data=plot1_data)

@app.route("/plot")
def plot_png2():
    # Generate the figure **without using pyplot**.
    fig = Figure(figsize=(20, 10), dpi=100)
    ax = fig.subplots()
    worldmap = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    worldmap.plot(color="lightgrey", ax=ax)
    x = np.arange(-50,50)
    ax.scatter(x,x)
    # Save it to a temporary buffer.
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
    
    

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x = np.arange(30)
    axis.plot(x, x)
    return fig





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

