import os
from flask import Flask, render_template
from weather_hero.weather_hero import WeatherHero
# from models import init_db, save_run_record, get_history

app = Flask(__name__)

# Initialize SQLite DB
# init_db()

@app.route("/")
def index():
    # history = get_history()
    return render_template("index.html")

@app.route("/run")
def run_analysis():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.join(parent_dir, '3270')
    data_path = os.path.join(base_dir, 'data', 'test.csv') 
    output_path = os.path.join(base_dir, 'data', 'summary.csv')
    analyzer = WeatherHero(data_path, output_path)

    plot_paths = analyzer.process_weather_data()

    # Save to DB
    # save_run_record(results)

    return render_template(
        "results.html",
        plot_paths=plot_paths
    )

if __name__ == "__main__":
    app.run(debug=True)
