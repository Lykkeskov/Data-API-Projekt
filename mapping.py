import pandas as pd
import json
import plotly.express as px
import plotly.io as pio
from PIL import Image
import plotly.graph_objects as go

class PlanKort:
    def __init__(self, etage_data: dict, billededata: pd.DataFrame):
        self.etager = etage_data
        self.data = billededata
        self.image_sizes = {}

        # find størrelser for hver etage
        for floor, path in self.etager.items():
            img = Image.open(path)  # skal være filsystem path fx "static/plan1.png"
            self.image_sizes[floor] = img.size

    def lav_figur(self):
        choropleth = go.Figure()

        lokaleLokationer = json.load(open('1stEtage.geojson'))
        lokaleData = {}
        for feature in lokaleLokationer['features']:
            feature['id'] = feature["properties"]["room"]

        lysData = pd.read_csv("sejedata.csv")
        lysData.rename(columns={"lokale": "room"}, inplace=True)

        maxLysNiveau = 300
        if lysData["lys_niveau"].max() > maxLysNiveau:
            maxLysNiveau = lysData["lys_niveau"].max()

        halvLysNiveau = maxLysNiveau / 2

        # tilføj en scatter trace per etage
        for i, (floor, path) in enumerate(self.etager.items()):
            etage_data = self.data[self.data["etage"] == floor]
            width, height = self.image_sizes[floor]

            choropleth.add_trace(go.Scatter(
                x=etage_data["x"],
                y=etage_data["y"],
                mode="markers+text",
                text=etage_data["lokale"],
                marker=dict(
                    color=etage_data["lys_niveau"],
                    size=12,
                    colorscale="RdYlGn",
                    colorbar=dict(title="Lys niveau", x=1.5, y=0.5) if i == 0 else None
                ),
                name=f"Etage {floor}",
                visible=(i == 0)  # start med at vise stueetagen
            ))

        maxLysNiveau = 300
        if lysData["lys_niveau"].max() > maxLysNiveau:
            maxLysNiveau = lysData["lys_niveau"].max()


        # dropdown menu
        updatemenus = [dict(
            buttons=[],
            direction="down",
            showactive=True,
            x=0.1, y=1.15
        )]



        for i, (floor, path) in enumerate(self.etager.items()):
            width, height = self.image_sizes[floor]

            # vis kun den her etage
            visibility = [False] * len(self.etager)
            visibility[i] = True

            first_floor, first_path = list(self.etager.items())[0]
            width, height = self.image_sizes[first_floor]
            choropleth.add_layout_image(
                dict(
                    source=f"/{first_path}",
                    xref="x",
                    yref="y",
                    x=0, y=height,
                    sizex=2339, sizey=3309,
                    sizing="stretch",
                    layer="below"
                )
            )

            updatemenus[0]["buttons"].append(dict(
                label=f"Etage {floor}",
                method="update",
                args=[
                    {"visible": visibility},
                    {"images": [dict(
                        source=f"/{path}",
                        xref="x",
                        yref="y",
                        x=0, y=height,
                        sizex=2339, sizey=3309,
                        sizing="stretch",
                        layer="below"
                    )],
                        "xaxis": dict(visible=False, range=[0, width]),
                        "yaxis": dict(visible=False, range=[0, height], scaleanchor="x")
                    }
                ]
            ))
            for feature in lokaleLokationer["features"]:
                coords = feature["geometry"]["coordinates"][0]
                room = feature["properties"]["room"]

                if room in lysData["room"].values:
                    lys_value = lysData.loc[lysData["room"] == room, "lys_niveau"].values[0]
                else:
                    lys_value = None

                if lys_value is not None:
                    if lys_value <= halvLysNiveau:
                        afstand = (halvLysNiveau - lys_value) * 255 / halvLysNiveau
                        fillcolor = f"rgba({int(255)}, {int(255 - afstand)}, {int(0)}, {1})"

                    if lys_value > halvLysNiveau:
                        afstand = (lys_value - halvLysNiveau) * 255 / halvLysNiveau
                        fillcolor = f"rgba({int(255 - afstand)}, {int(255)}, {int(0)}, {1})"
                else:
                    fillcolor = "rgba(0,0,0,1)"

                x, y = zip(*coords)
                choropleth.add_trace(go.Scatter(
                    x=x,
                    y=y,
                    fill="toself",
                    fillcolor=fillcolor,
                    line=dict(color="black"),
                    name=room,
                    text=f"{room}: {lys_value}",
                    hoverinfo="text"
                ))

        choropleth.update_layout(updatemenus=updatemenus)
        return choropleth
