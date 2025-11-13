from datetime import datetime
import os
from flask import Flask, render_template, request
from weather_hero.weather_hero import WeatherHero
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- Database configuration ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "weather_hero.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    history = Record.query.order_by(Record.timestamp.desc()).all()
    run_count = Record.query.count()
    return render_template("index.html", history=history, run_count=run_count)

@app.route("/run", methods=['POST'])
def run_analysis():
    name = request.form["name"]
    reason = request.form["reason"]

    new_record = Record(name=name, reason=reason)
    db.session.add(new_record)
    db.session.commit()

    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.join(parent_dir, '3270')
    data_path = os.path.join(base_dir, 'data', 'test.csv') 
    output_path = os.path.join(base_dir, 'data', 'summary.csv')
    analyzer = WeatherHero(data_path, output_path)

    plot_paths = analyzer.process_weather_data()
    return render_template(
        "results.html",
        plot_paths=plot_paths
    )

if __name__ == "__main__":
    app.run(debug=True)
