import plotly
import pandas as pd

floor1 = "static/plan1.png"
floor2 = "static/plan2.png"
floor3 = "static/plan3.png"
floor4 = "static/plan4.png"

billededata = pd.DataFrame({
    'etage':[floor1, floor2, '''floor3,floor4'''],
    'lokale':["D2111","D2221"],
    'x':[50,60],
    'y':[50,60]
})

etage = 1
etage_data = billededata[billededata["etage"] == etage]

fig = px.scatter(
    etage_data,
    x="x", y="y",
    color="lys_niveau",
    text="lokale",
    color_continuous_scale="YlOrRd"
)

fig.update_layout(
    billeder=[dict(
        source=etage_data,
        x_reference="x",
        y_reference="y",
        x=0, y=300,
        sizex=300, sizey=300,
        sizing="stretch",
        layer="below"
    )]
)