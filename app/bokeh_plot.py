"""  https://www.kaggle.com/kevinchiha/interactive-bokeh-plot-nba-dataset/data
"""

from bokeh.plotting import figure
from bokeh.plotting import ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.models import HoverTool
from bokeh.layouts import row, column
from bokeh.layouts import widgetbox
from bokeh.models import Slider, Select, CustomJS, CheckboxGroup
from app.Season import Season
from bokeh.embed import components

from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from bokeh.resources import INLINE
from bokeh.models import LinearAxis


class BokehPlot:

    @classmethod
    def modify_doc(cls):
        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
        season = Season()
        seasons_1990_on = season.seasons_1990_on

        data_dict = seasons_1990_on.to_dict('list')

        source = ColumnDataSource(data=data_dict)


        years = seasons_1990_on["Year"].unique().tolist()
        years = ["ALL"] + [str(int(year)) for year in years][::-1]

        slider = Slider(title="Year", start=1990, end=2017, step=1, value=2006)
        menu_options_list = ["ALL"] + seasons_1990_on["Tm"].unique().tolist()
        team_menu = Select(options=menu_options_list, value="ALL", title="Team")
        columns = list(seasons_1990_on.columns)
        x_axis_menu = Select(options=columns, value="3PA", title="X Axis")
        y_axis_menu = Select(options=columns, value="3P", title="Y Axis")
        y_axis_menu = Select(options=columns, value="3P", title="Y Axis")
        season_menu = Select(options=years, value="ALL", title="Season")

        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
        p1 = figure(
            tools=TOOLS
        )

        p1.xaxis.visible = None
        p1.yaxis.visible = None

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

        widgetboxes = [
            widgetbox(team_menu),
            widgetbox(season_menu),
            widgetbox(x_axis_menu),
            widgetbox(y_axis_menu)
        ]
        column1 = column(widgetboxes)
        layout = row(column1, p1)

        xaxis = LinearAxis(axis_label="3 Pointers Attempted")
        yaxis = LinearAxis(axis_label="3 Pointers Made")
        p1.add_layout(xaxis, 'below')
        p1.add_layout(yaxis, 'left')


        args = {
            'source': source,
            'data_dict': data_dict,
            'team_menu': team_menu,
            'slider': slider,
            'x_axis_menu': x_axis_menu,
            'y_axis_menu': y_axis_menu,
            'season_menu': season_menu,
            'p': p1,
            'xaxis': xaxis,
            'yaxis': yaxis,

        }

        callback = CustomJS(args=args, code="""
            data_copy = JSON.parse(JSON.stringify(data_dict))
            console.log(data_copy, "<-- Here is data copy");
            console.log(p)

            keys = Object.keys(data_copy)
            selected_team = team_menu.value
            selected_season = season_menu.value
            all_seasons = data_copy['Year']
            all_teams = data_copy['Tm']

            // remove_row removes a row of data
            // for all lists.
            function remove_row(index) {
                for (j = 0; j < keys.length; j++) {
                    column = data_copy[keys[j]]
                    value = column[index]
                    data_copy[keys[j]].splice(index, 1)
                }
            }

            // Filter Year
            if (selected_season !== "ALL") {

                for (var i = all_seasons.length - 1; i >= 0; i--) {
                    season = all_seasons[i];
                    if (season != selected_season) { 
                        remove_row(i)
                    }
                }

            }

            // Filter Team
            if (selected_team !== "ALL") {
                for (var i = all_teams.length - 1; i >= 0; i--) {
                    team_name = all_teams[i];
                    if (team_name !== selected_team) { 
                        remove_row(i)
                    }
                }
                console.log(data_copy['Tm'].length, "<--- End Length")
            }


            console.log("Here are the keys -->", keys)
            console.log("Here are team menu -->", team_menu)
            console.log("Here are slider  -->", slider)
            console.log("Here are x_axis_menu menu -->", x_axis_menu)
            console.log("Here are y_axis_menu menu -->", y_axis_menu)


            if (team_menu.value === "ALL") {    
                console.log("What's up. I am ALL");

            }


            data_copy['X'] = data_copy[x_axis_menu.value]
            data_copy['Y'] = data_copy[y_axis_menu.value]
            source.data = data_copy

            xaxis.attributes.axis_label = x_axis_menu.value
            yaxis.attributes.axis_label = y_axis_menu.value
            xaxis.change.emit();
            yaxis.change.emit();



            source.change.emit();
        """)

        x_axis_menu.js_on_change('value', callback)
        y_axis_menu.js_on_change('value', callback)
        slider.js_on_change('value', callback)
        team_menu.js_on_change('value', callback)
        season_menu.js_on_change('value', callback)


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