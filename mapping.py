import plotly.express as px
from PIL import Image

# hent billedets dimensioner
img = Image.open("static/plan1.png")
#{{ url_for('static', filename='style.css') }}
width, height = img.size

class PlanKort:
    def __init__(self, etage_data, billededata):
        self.floor_image = etage_data
        self.data = billededata

    def lav_figur(self):
        # scatter points
        fig = px.scatter(
            self.data,
            x="x", y="y",
            color="lys_niveau",
            text="lokale",
            color_continuous_scale="YlOrRd"
        )

        # vis plantegning som baggrund
        fig.update_layout(
            images=[dict(
                source=self.floor_image,
                xref="x",
                yref="y",
                x = 0, y = height,
                sizex = width, sizey = height,
                layer="below"
            )],
            xaxis=dict(visible=False, range=[0, width]),
            yaxis=dict(visible=False, range=[0, height], scaleanchor="x"),
        )
        return fig
