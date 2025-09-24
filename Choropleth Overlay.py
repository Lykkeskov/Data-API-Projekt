import json
import pandas as pd
import plotly.express as px
import plotly.io as pio
from PIL import Image
import plotly.graph_objects as go


pio.renderers.default = "browser"

#Data formateres som variabler
lokaleLokationer = json.load(open('1stEtage.geojson'))
lokaleData = {}
for feature in lokaleLokationer['features']:
    feature['id'] = ["properties"]["room"]
    lokaleData[feature['properties']['st_nm']] = feature['id']

lysData = pd.read_csv("sejedata.csv")


#Etablere pathfilen
pathfile = "static/plan1.png"

fig = go.Figure()
pyLogo = Image.open(pathfile)

#Få dimensionerne på billedet
def get_num_pixels(filepath):
    width, height = Image.open(filepath).size
    return width, height

imageWidth, imageHeight = get_num_pixels(pathfile)


# Add trace

fig.add_layout_image(
        dict(
            source=pyLogo,
            xref="x",
            yref="y",
            x=0,
            y=imageHeight,
            sizex = imageWidth,
            sizey = imageHeight,
            opacity=1,
            layer="below"))

fig.show()
print(lokaleLokationer["features"][1]["geometry"]["coordinates"])