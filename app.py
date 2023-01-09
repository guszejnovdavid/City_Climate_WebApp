from flask import Flask, request, Response
import config
import numpy as np
import io
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
sns.set()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/plot')
def plot_png():
    output = io.BytesIO()
    FigureCanvas(plt.gcf()).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

# @app.route("/mongo_health")
# def mongo_health():
    # db = mongo_client.test
    # ok = db.command("ping").get("ok")
    # return "<p>MongoDB health check: {}</p>".format(ok)

# @app.route("/redis_health")
# def redis_health():
    # ok = redis_client.ping()
    # return "<p>Redis health check: {}</p>".format(ok)   

# @app.route('/send_mail', methods=['GET'])
# def send_mail():
    # email = request.args.get('email')
    # tasks.send_mail_async.apply_async(args=[email], countdown=3)
    # return "<p>Email sent to {}</p>".format(email)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=config.APP_SERVER_PORT)
    




from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

