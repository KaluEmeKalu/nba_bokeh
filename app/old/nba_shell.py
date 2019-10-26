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
