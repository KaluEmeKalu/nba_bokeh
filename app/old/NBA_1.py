"""  https://www.kaggle.com/kevinchiha/interactive-bokeh-plot-nba-dataset/data
"""

import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.plotting import ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.models import HoverTool
from bokeh.layouts import row, column
from bokeh.io import curdoc
from bokeh.layouts import widgetbox
from bokeh.models import Slider, Select


TOOLS = "pan,wheel_zoom,box_zoom,reset,save"


players = pd.read_csv("Players.csv")
seasons = pd.read_csv("Seasons_Stats.csv")

players.drop(players.columns[0], axis=1, inplace=True)
seasons.drop(seasons.columns[0], axis=1, inplace=True)

players.dropna(how="all", inplace=True)
seasons.dropna(how="all", inplace=True)
players = players[players.birth_city.notnull()]

seasons_1990_on = seasons[seasons.Year >= 1990]
seasons_1990_on = seasons_1990_on[
    (seasons_1990_on["3P%"].notnull())
    & (seasons_1990_on["3P%"] > 0)
    & (seasons_1990_on["3P"].notnull())
    & (seasons_1990_on["3P"] > 0)
    & (seasons_1990_on["3PA"].notnull())
    & (seasons_1990_on["3PA"] > 0)
    & (seasons_1990_on["GS"] > 0)
    & (seasons_1990_on["G"].notnull())
    & (seasons_1990_on["G"] > 0)
    & (seasons_1990_on["2PA"].notnull())
    & (seasons_1990_on["2PA"] > 0)
    & (seasons_1990_on["2P"].notnull())
    & (seasons_1990_on["2P"] > 0)
]

new_index = np.arange(0, len(seasons_1990_on)).tolist()
seasons_1990_on.index = new_index

color_dict = {
    "VAN": "Blue",
    "MIL": "Red",
    "LAC": "Yellow",
    "BOS": "Purple",
    "SAC": "Silver",
    "HOU": "Magenta",
    "POR": "Green",
    "CHI": "CornFlowerBlue",
    "ORL": "Chocolate",
    "SEA": "Coral",
    "GSW": "Crimson",
    "TOR": "DarkCyan",
    "TOT": "Gold",
    "MIA": "GreenYellow",
    "MIN": "HotPink",
    "LAL": "Khaki",
    "NJN": "Lavender",
    "DAL": "LightSkyBlue",
    "PHO": "Orange",
    "NYK": "MediumAquamarine",
    "CHH": "OrangeRed",
    "IND": "PaleVioletRed",
    "SAS": "SpringGreen",
    "UTA": "YellowGreen",
    "CLE": "RoyalBlue",
    "WAS": "SteelBlue",
    "DEN": "RoseBrown",
    "DET": "IndianRed",
    "PHI": "Salmon",
    "ATL": "DarkOrchid",
    "MEM": "Tomato",
    "NOH": "DarkKhaki",
    "CHA": "MediumSeaGreen",
    "NOK": "OliveDrab",
    "OKC": "Orange",
    "BRK": "Blue",
    "NOP": "PowderBlue",
    "CHO": "Navy",
}
palette = [
    "aliceblue",
    "antiquewhite",
    "aqua",
    "aquamarine",
    "azure",
    "beige",
    "bisque",
    "black",
    "blanchedalmond",
    "blue",
    "blueviolet",
    "brown",
    "burlywood",
    "cadetblue",
    "chartreuse",
    "chocolate",
    "coral",
    "cornflowerblue",
    "cornsilk",
    "crimson",
    "cyan",
    "darkblue",
    "darkcyan",
    "darkgoldenrod",
    "darkgray",
    "darkgreen",
    "darkkhaki",
    "darkmagenta",
    "darkolivegreen",
    "darkorange",
    "darkorchid",
    "darkred",
    "darksalmon",
    "darkseagreen",
    "darkslateblue",
    "darkslategray",
    "darkturquoise",
    "darkviolet",
    "red",
]

color_mapper = CategoricalColorMapper(
    factors=seasons_1990_on["Tm"].unique().tolist(), palette=palette
)

p1 = figure(
    x_axis_label="3 Points Attempted", y_axis_label="3 Points Made", tools=TOOLS
)
p2 = figure(
    x_axis_label="2 Points Attempted", y_axis_label="2 Points Made", tools=TOOLS
)

slider = Slider(title="Year", start=1990, end=2017, step=1, value=2006)
menu_options_list = ["ALL"] + seasons_1990_on["Tm"].unique().tolist()
menu = Select(
    options=menu_options_list, value="GSW", title="Team"
)

source = ColumnDataSource(
    data={
        "x_3p": seasons_1990_on["3PA"],
        "y_3p": seasons_1990_on["3P"],
        "Tm": seasons_1990_on["Tm"],
        "x_2p": seasons_1990_on["2PA"],
        "y_2p": seasons_1990_on["2P"],
        "Year": seasons_1990_on["Year"],
        "Player": seasons_1990_on["Player"],
    }
)


def callback(attr, old, new):

    if menu.value == 'ALL':

        new_x_3p = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
        ]["3PA"]
        new_y_3p = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
        ]["3P"]
        new_tm = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
        ]["Tm"]
        new_x_2p = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
        ]["2PA"]
        new_y_2p = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
        ]["2P"]
        new_year = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
        ]["Year"]
        new_player = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
        ]["Player"]
    else:
        new_x_3p = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
        ]["3PA"]
        new_y_3p = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
            & (seasons_1990_on["Tm"] == menu.value)
        ]["3P"]
        new_tm = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
            & (seasons_1990_on["Tm"] == menu.value)
        ]["Tm"]
        new_x_2p = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
            & (seasons_1990_on["Tm"] == menu.value)
        ]["2PA"]
        new_y_2p = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
            & (seasons_1990_on["Tm"] == menu.value)
        ]["2P"]
        new_year = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
            & (seasons_1990_on["Tm"] == menu.value)
        ]["Year"]
        new_player = seasons_1990_on[
            (seasons_1990_on["Year"] == slider.value)
            & (seasons_1990_on["Tm"] == menu.value)
        ]["Player"]

    source.data = {
        "x_3p": new_x_3p,
        "y_3p": new_y_3p,
        "Tm": new_tm,
        "x_2p": new_x_2p,
        "y_2p": new_y_2p,
        "Year": new_year,
        "Player": new_player,
    }


slider.on_change("value", callback)
menu.on_change("value", callback)

###################
p1.circle(
    "x_3p",
    "y_3p",
    source=source,
    alpha=0.8,
    nonselection_alpha=0.1,
    color=dict(field="Tm", transform=color_mapper),
    legend="Tm",
)

p1.legend.location = "bottom_right"
####################

####################
p2.circle(
    "x_2p",
    "y_2p",
    source=source,
    alpha=0.8,
    nonselection_alpha=0.1,
    color=dict(field="Tm", transform=color_mapper),
    legend="Tm",
)

p2.legend.location = "bottom_right"
#######################

hover1 = HoverTool(tooltips=[("Player", "@Player")])
p1.add_tools(hover1)
hover2 = HoverTool(tooltips=[("Player", "@Player")])
p2.add_tools(hover2)

column1 = column(widgetbox(menu), widgetbox(slider))
layout = row(column1, p1, p2)

curdoc().add_root(layout)

NBA_1.py
