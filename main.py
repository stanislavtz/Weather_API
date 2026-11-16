from flask import Flask, render_template, jsonify, request, redirect, url_for
import pandas as pd
from werkzeug.utils import redirect

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        station_id = request.form["station_id"]
        date = request.form["date"]

        return redirect(url_for("weather", station_id=station_id, date=date))
    return render_template('home.html')


@app.get("/weather/<int:station_id>/<string:date>")
def weather(station_id, date):
    try:
        df = pd.read_csv(f"data/TG_STAID{station_id:06d}.txt",
                         skiprows=20,
                         parse_dates=["    DATE"],)

        df.columns = [column.strip() for column in df.columns]
        clear_df = df.loc[df["TG"] != -9999].copy()
        temperature = clear_df.loc[clear_df["DATE"] == date]["TG"].squeeze()

        try:
            temperature = float(temperature) / 10
        except TypeError:
            temperature = None

        station_df = pd.read_csv("data/stations.txt", skiprows=17)
        station_df = station_df[:50]
        station_df.columns = [column.strip() for column in station_df.columns]

        station_name = station_df.loc[station_df["STAID"] == station_id]["STANAME"].squeeze()

        return jsonify({
            'station_id': station_id,
            "station name": station_name,
            'date': date,
            'temperature': temperature
        })
    except FileNotFoundError:
        return jsonify({"info": f"No data for station {station_id}"})


if __name__ == '__main__':
    app.run(debug=True)