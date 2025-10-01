import plotly.graph_objects as go
import pandas as pd
from PIL import Image


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
        fig = go.Figure()

        # tilføj en scatter trace per etage
        for i, (floor, path) in enumerate(self.etager.items()):
            etage_data = self.data[self.data["etage"] == floor]
            width, height = self.image_sizes[floor]

            fig.add_trace(go.Scatter(
                x=etage_data["x"],
                y=etage_data["y"],
                mode="markers+text",
                text=etage_data["lokale"],
                marker=dict(
                    color=etage_data["lys_niveau"],
                    size=12,
                    colorscale="YlOrRd",
                    colorbar=dict(title="Lys niveau") if i == 0 else None
                ),
                name=f"Etage {floor}",
                visible=(i == 0)  # start med at vise stueetagen
            ))

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

        fig.update_layout(updatemenus=updatemenus)
        return fig
