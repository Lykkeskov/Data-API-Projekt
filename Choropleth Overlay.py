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
    feature['id'] = feature["properties"]["room"]

lysData = pd.read_csv("sejedata.csv")
lysData.rename(columns={"lokale": "room"}, inplace=True)


#Får dimensionerne på billedet
def get_num_pixels(filepath):
    width, height = Image.open(filepath).size
    return width, height

#Finder max værdien som bruges til at modellere vores Red-Yellow-Green skala
maxLysNiveau = 300
if lysData["lys_niveau"].max() > maxLysNiveau:
    maxLysNiveau = lysData["lys_niveau"].max()

halvLysNiveau = maxLysNiveau / 2

#Etablere pathfilen
pathfile = "static/plan1.png"
pyLogo = Image.open(pathfile)
imageWidth, imageHeight = get_num_pixels(pathfile)


fig = go.Figure()


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

for feature in lokaleLokationer["features"]:
    coords = feature["geometry"]["coordinates"][0]
    room = feature["properties"]["room"]

    if room in lysData["room"].values:
        lys_value = lysData.loc[lysData["room"] == room, "lys_niveau"].values[0]
    else:
        lys_value = None

    if lys_value is not None:
        if lys_value <= halvLysNiveau:
            afstand = (halvLysNiveau - lys_value) * 255/halvLysNiveau
            fillcolor = f"rgba({int(255)}, {int(255-afstand)}, {int(0)}, {1})"

        if lys_value > halvLysNiveau:
            afstand = (lys_value - halvLysNiveau) * 255/halvLysNiveau
            fillcolor = f"rgba({int(255-afstand)}, {int(255)}, {int(0)}, {1})"
    else:
        fillcolor = "rgba(200,200,200,0.3)"

    x, y = zip(*coords)
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        fill="toself",
        fillcolor=fillcolor,
        line=dict(color="black"),
        name=room,
        text=f"{room}: {lys_value}",
        hoverinfo="text"
    ))

# --- Axes ---
fig.update_xaxes(scaleanchor="y", showgrid=False, visible=False)
fig.update_yaxes(showgrid=False, visible=False)

fig.show()

print(lokaleLokationer["features"][1]["geometry"]["coordinates"])