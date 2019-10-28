import json
import pandas as pd


def get_data(filename="app/data/nba2018-2019.json"):
    with open(filename, 'r') as f:
        data = f.read()
    d = json.loads(data)
    players = d['resultSets'][0]['rowSet']
    cols = d['resultSets'][0]['headers']

    data = {col: [] for col in cols}
    for player in players:
        for index, stat in enumerate(player):
            col = cols[index]
            data[col].append(stat)

    df = pd.DataFrame.from_dict(data)
    return df
 