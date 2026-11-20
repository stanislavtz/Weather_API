import numpy as np
from flask import Flask, render_template, jsonify, request, redirect, url_for
import pandas as pd
from werkzeug.utils import redirect


def get_station_name(station_id):
    station_df = pd.read_csv("data/stations.txt", skiprows=17)
    station_df = station_df[:44]
    station_df.columns = [column.strip() for column in station_df.columns]

    station_name = station_df.loc[station_df["STAID"] == station_id]["STANAME"].squeeze()
    station_name = station_name.strip()

    return station_name


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Home page of the API. Allow user to add station id and date and to
    retrieve data for that date.
    Also renders a table with all stations IDs and Names."""
    if request.method == "POST":
        station_id = request.form["station_id"]
        date = request.form["date"]

        return redirect(url_for("weather", station_id=station_id, date=date))

    df = pd.read_csv("data/stations.txt", skiprows=17)
    df.columns = [column.strip() for column in df.columns]

    stations_df = df.iloc[:, :2][:44]

    # stations = []
    # for station in stations_id_and_names_df.iterrows():
    #     stations.append((station[0], station[1]["STAID"], station[1]["STANAME"]))

    return render_template('home.html', stations=stations_df.to_html())


@app.get("/weather/api/v1/<int:station_id>/")
def all_weathers(station_id):
    """Retrieves all weather data for a specific station"""
    df = pd.read_csv(f"data/TG_STAID{station_id:06d}.txt",
                     skiprows=20,
                     parse_dates=["    DATE"])
    df.columns = [column.strip() for column in df.columns]

    df_copy = df.copy()
    df_copy["TG"] = df["TG"] / 10
    df_copy.loc[df["TG"] == -9999, "TG"] = np.nan

    return df_copy.to_dict(orient="records")


@app.get("/weather/api/v1/<int:station_id>/<string:date>/")
def weather(station_id, date):
    """Retrieves weather data for a specific station on particular date."""
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

        name = get_station_name(station_id)

        return jsonify({
            'station_id': station_id,
            "station name": name,
            'date': date,
            'temperature': temperature
        })
    except FileNotFoundError:
        return jsonify({"info": f"No data for station {station_id}"})


@app.get("/weather/api/v1/yearly/<int:station_id>/<int:year>/")
def yearly(station_id, year):
    """Retrieve data for specific station for whole year"""
    df = pd.read_csv(f"data/TG_STAID{station_id:06d}.txt",
                     skiprows=20,
                     parse_dates=["    DATE"])
    df.columns = [column.strip() for column in df.columns]

    yearly_df = df[df["DATE"].dt.year == year]

    return yearly_df.to_dict(orient="records")


if __name__ == '__main__':
    app.run(debug=True)