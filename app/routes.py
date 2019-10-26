from app import app
from flask import render_template, flash, url_for
from bokeh.embed import server_document

from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from app.bokeh_plot import BokehPlot





@app.route('/test', methods=['GET'])
def bkapp_page():
    from threading import Thread
    try:
        Thread(target=BokehPlot.bk_worker).start()
    except Exception as e:
        print(e)

    script = server_document('http://localhost:5006/bkapp')
    print(script)
    return render_template("embed.html", script=script, template="Flask")



@app.route('/', methods=['GET'])
def test():
    context = BokehPlot.modify_doc()
    return render_template("embed2.html", **context)
