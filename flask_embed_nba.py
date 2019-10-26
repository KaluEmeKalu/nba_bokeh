from flask import Flask, render_template

from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from tornado.ioloop import IOLoop
from BokehPlot import modify_doc

from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature

app = Flask(__name__)



def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    print("Here is modify doc: {}".format(modify_doc))
    try:
        server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
        server.start()
        server.io_loop.start()
    except Exception as e:
        print(e)




@app.route('/', methods=['GET'])
def bkapp_page():
    from threading import Thread
    try:
        Thread(target=bk_worker).start()
    except Exception as e:
        print(e)

    script = server_document('http://localhost:5006/bkapp')
    print(script)
    return render_template("embed.html", script=script, template="Flask")




if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=8000)
