from flask import Flask, render_template
import pandas as pd
from mapping import PlanKort

app = Flask(__name__)

@app.route('/')
def index():
    # lokale data
    billededata = pd.DataFrame({
        'etage': [1, 2, 3, 4],
        'lokale': ["D2111", "D2221", "D2321", "D2401"],
        'x': [1392, 1000, 1400, 60],
        'y': [2914, 1200, 70, 400],
        'lys_niveau': [300, 1000, 500, 299]
    })

    etager = {
        1: "static/plan1.png",
        2: "static/plan2.png",
        3: "static/plan3.png",
        4: "static/plan4.png"
    }


    # lav plankort objekt
    fm = PlanKort(etager, billededata)
    fig = fm.lav_figur()

    # konverter plankort til html så vi kan website stuff :)
    graph_html = fig.to_html(full_html = False)
    return render_template("index.html", graph_html=graph_html)

# kør den app der
if __name__ == '__main__':
    app.run(debug=True)
