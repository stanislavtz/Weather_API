from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return render_template('home.html')


@app.get("/weather/<int:station_id>/<string:date>")
def weather(station_id, date):
    temperature = 23
    return jsonify({
        'station_id': station_id,
        'date': date,
        'temperature': temperature
    })


if __name__ == '__main__':
    app.run(debug=True)