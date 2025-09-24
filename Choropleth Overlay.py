import json
import pandas as pd
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"
lokaleLokationer = json.load(open('1stEtage.geojson'))



print(lokaleLokationer["features"][1]["geometry"]["coordinates"])