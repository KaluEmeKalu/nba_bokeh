from app import app
from flask import render_template, flash, url_for
from bokeh.embed import server_document

from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from app.bokeh_plot import BokehPlot





@app.route('/', methods=['GET'])
def bkapp_page():
    from threading import Thread
    try:
        Thread(target=BokehPlot.bk_worker).start()
    except Exception as e:
        print(e)

    script = server_document('http://localhost:5006/bkapp')
    print(script)
    return render_template("embed.html", script=script, template="Flask")
