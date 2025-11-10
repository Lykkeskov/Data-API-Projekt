from flask import Flask, render_template
import pandas as pd
import sqlite3 as sql
from mapping import PlanKort

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to SQLite database
    conn = sql.connect("Lysniveau.db")

    # Load lokaledata table into a pandas DataFrame
    billededata = pd.read_sql_query("SELECT * FROM lokaledata", conn)

    # Close connection
    conn.close()

    # Define etage images
    etager = {
        1: "static/plan1.png",
        2: "static/plan2.png",
        3: "static/plan3.png",
        4: "static/plan4.png"
    }

    # Create PlanKort object
    fm = PlanKort(etager, billededata)
    choroplethFigur = fm.lav_figur()

    # Convert figure to HTML
    graph_html = choroplethFigur.to_html(full_html=False)
    return render_template("index.html", graph_html=graph_html)

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
