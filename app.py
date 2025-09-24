from flask import Flask, render_template
import pandas as pd
from mapping import PlanKort

app = Flask(__name__)

@app.route('/')
def index():
    # lokale data
    billededata = pd.DataFrame({
        # 'etage': [floor1, floor2, '''floor3,floor4'''],
        'lokale': ["D2111", "D2221"],
        'x': [1392, 150],
        'y': [2914, 120],
        'lys_niveau': [300, 150]
    })

    source = "/static/plan1.png"
    floor2 = "static/plan2.png"
    floor3 = "static/plan3.png"
    floor4 = "static/plan4.png"

    # lav plankort objekt
    fm = PlanKort(source, billededata)
    fig = fm.lav_figur()

    # konverter plankort til html så vi kan website stuff
    graph_html = fig.to_html(full_html = False)

    return render_template("index.html", graph_html=graph_html)

# kør den app der
if __name__ == '__main__':
    app.run(debug=True)
