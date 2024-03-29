"""  https://www.kaggle.com/kevinchiha/interactive-bokeh-plot-nba-dataset/data
"""

from bokeh.plotting import figure
from bokeh.plotting import ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.models import HoverTool
from bokeh.layouts import row, column
from bokeh.layouts import widgetbox
from bokeh.models import Slider, Select, CustomJS
from app.Season import Season
from bokeh.embed import components

from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from bokeh.resources import INLINE


class BokehPlot:

    @classmethod
    def modify_doc(cls):
        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
        season = Season()
        seasons_1990_on = season.seasons_1990_on

        data_dict = seasons_1990_on.to_dict('list')

        source = ColumnDataSource(data=data_dict)

        slider = Slider(title="Year", start=1990, end=2017, step=1, value=2006)
        menu_options_list = ["ALL"] + seasons_1990_on["Tm"].unique().tolist()
        team_menu = Select(options=menu_options_list, value="ALL", title="Team")
        columns = list(seasons_1990_on.columns)
        x_axis_menu = Select(options=columns, value="3PA", title="X Axis")
        y_axis_menu = Select(options=columns, value="3P", title="Y Axis")

        palette = season.get_palette()
        color_mapper = CategoricalColorMapper(
            factors=seasons_1990_on["Tm"].unique().tolist(),
            palette=palette
        )

        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
        p1 = figure(
            x_axis_label="3 Points Attempted",
            y_axis_label="3 Points Made",
            tools=TOOLS
        )

        ###################
        p1.circle(
            "X",
            "Y",
            source=source,
            alpha=0.8,
            nonselection_alpha=0.1,
        )

        p1.legend.location = "bottom_right"
        ####################

        ####################


        #######################
        cls.add_tooltips(p1)


        column1 = column(widgetbox(team_menu), widgetbox(slider), widgetbox(x_axis_menu), widgetbox(y_axis_menu))
        layout = row(column1, p1)
        args = {
            'source': source,
            'data_dict': data_dict,
            'team_menu': team_menu,
            'slider': slider,
            'x_axis_menu': x_axis_menu,
            'y_axis_menu': y_axis_menu
        }

        callback = CustomJS(args=args, code="""

            data_copy = JSON.parse(JSON.stringify(data_dict))
            console.log(data_copy, "<-- Here is data copy");
            if (team_menu.value === "ALL") {
                console.log("What's up. I am ALL");
            }

            source.change.emit();
        """)

        x_axis_menu.js_on_change('value', callback)


        resources = INLINE.render()

        script, div = components({'p': layout})

        return {'script': script, 'div': div, 'resources': resources}

        def callback(attr, old, new):
            if menu.value == "ALL":
                new_df = seasons_1990_on[seasons_1990_on['Year'] == slider.value]
                new_x = new_df[x_axis_menu.value]
                new_y = new_df[y_axis_menu.value]

            else:
                new_df = seasons_1990_on[
                    (seasons_1990_on['Year'] == slider.value) &
                    (seasons_1990_on['Tm'] == menu.value)
                ]
                new_x = new_df[x_axis_menu.value]
                new_y = new_df[y_axis_menu.value]

            source.data['X'] = new_x
            source.data['Y'] = new_y

            new_df['X'] = new_x
            new_df['Y'] = new_y

            tooltips = [
                ("Players", "@Player"),
                (x_axis_menu.value, "@{}".format(x_axis_menu.value))
                (y_axis_menu.value, "@{}".format(y_axis_menu.value))

            ]

            source.data = new_df

            cls.add_tooltips(plot=p1, tooltips=tooltips)

            print("Here is x", new_x)
            print("Here is y", new_y)
            print("Here is y name", new_y.name)
            p1.xaxis.axis_label = new_x.name
            p1.yaxis.axis_label = new_y.name

        slider.on_change("value", callback)
        menu.on_change("value", callback)
        x_axis_menu.on_change("value", callback)
        y_axis_menu.on_change("value", callback)

    @staticmethod
    def add_tooltips(plot, tooltips=False):
        if not tooltips:
            tooltips = [
                ("Player", "@Player"),
                ("X", "@X"),
                ("Y", "@Y"),
            ]

        hover1 = HoverTool(tooltips=tooltips)
        plot.add_tools(hover1)
        return plot

    @classmethod
    def bk_worker(cls):
        # Can't pass num_procs > 1 in this configuration. If you need to run multiple
        # processes, see e.g. flask_gunicorn_embed.py
        print("Here is modify doc: {}".format(cls.modify_doc))
        try:
            server = Server({'/bkapp': cls.modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
            server.start()
            server.io_loop.start()
        except Exception as e:
            print(e)