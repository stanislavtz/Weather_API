from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def index():
    return render_template('home.html')


@app.get("/weather/<int:station_id>/<string:date>")
def weather(station_id, date):
    return render_template("weather.html",
                           station_id=station_id,
                           date=date)


if __name__ == '__main__':
    app.run(debug=True)