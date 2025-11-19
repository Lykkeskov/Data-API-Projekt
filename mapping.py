import pandas as pd
import json
import sqlite3 as sql
import plotly.graph_objects as go
from PIL import Image

class PlanKort:
    def __init__(self, etage_data: dict, billededata: pd.DataFrame):
        self.etager = etage_data
        self.data = billededata
        self.image_sizes = {}

        # Find størrelse for hver etage
        for floor, path in self.etager.items():
            img = Image.open(path)
            self.image_sizes[floor] = img.size

    def lav_figur(self):
        choropleth = go.Figure()

        #Load geojson (lokaler)
        lokaleLokationer = json.load(open('1stEtage.geojson'))
        for feature in lokaleLokationer['features']:
            feature['id'] = feature["properties"]["room"]

        # Hent lysdata fra SQLite i stedet for CSV
        conn = sql.connect("Lysniveau.db")
        lysData = pd.read_sql_query("SELECT etage, lokale AS room, x, y, lys_niveau FROM lokaledata", conn)
        conn.close()

        # Find maks og halv lysniveau
        maxLysNiveau = max(300, lysData["lys_niveau"].max())
        halvLysNiveau = maxLysNiveau / 2

        # Tilføj scatter traces til hevr etage
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
                visible=(i == 0)  # Kun første etage vises som standard
            ))

        # Tilføj første etages baggrundsbillede en gang
        first_floor, first_path = list(self.etager.items())[0]
        first_width, first_height = self.image_sizes[first_floor]
        choropleth.add_layout_image(
            dict(
                source=f"/{first_path}",
                xref="x",
                yref="y",
                x=0, y=first_height,
                sizex=first_width, sizey=first_height,
                sizing="stretch",
                layer="below"
            )
        )

        # Dropdown-menu
        updatemenus = [dict(
            buttons=[],
            direction="down",
            showactive=True,
            x=0.1, y=1.15
        )]

        # For hver etage: tilføj knap, polygoner og opdateringslogik
        for i, (floor, path) in enumerate(self.etager.items()):
            width, height = self.image_sizes[floor]
            visibility = [False] * len(self.etager)
            visibility[i] = True

            # Tilføj dropdown-knap for denne etage
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
                        sizex=width, sizey=height,
                        sizing="stretch",
                        layer="below"
                    )],
                        "xaxis": dict(visible=False, range=[0, width]),
                        "yaxis": dict(visible=False, range=[0, height], scaleanchor="x")
                    }
                ]
            ))

            # Tilføj rum-polygons (farvet efter lysniveau)
            for feature in lokaleLokationer["features"]:
                coords = feature["geometry"]["coordinates"][0]
                room = feature["properties"]["room"]

                lys_value = lysData.loc[lysData["room"] == room, "lys_niveau"].values[0] \
                    if room in lysData["room"].values else None

                if lys_value is not None:
                    if lys_value <= halvLysNiveau:
                        afstand = (halvLysNiveau - lys_value) * 255 / halvLysNiveau
                        fillcolor = f"rgba(255, {int(255 - afstand)}, 0, 1)"
                    else:
                        afstand = (lys_value - halvLysNiveau) * 255 / halvLysNiveau
                        fillcolor = f"rgba({int(255 - afstand)}, 255, 0, 1)"
                else:
                    fillcolor = "rgba(0,0,0,1)"

                x, y = zip(*coords)
                choropleth.add_trace(go.Scatter(
                    x=x, y=y,
                    fill="toself",
                    fillcolor=fillcolor,
                    line=dict(color="black"),
                    name=room,
                    text=f"{room}: {lys_value}",
                    hoverinfo="text",
                    visible=(i == 0)  # vis kun polygoner for første etage
                ))

        # ilføj dropdown-menu til layout
        choropleth.update_layout(updatemenus=updatemenus)
        return choropleth
