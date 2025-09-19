import plotly.express as px

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
                x=0, y=300,
                sizex=300, sizey=300,
                sizing="stretch",
                layer="below"
            )],
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
