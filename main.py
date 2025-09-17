from weather_hero import WeatherHero
import os

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'Weather Test Data.csv')
    output_path = os.path.join(base_dir, 'data', 'Weather Summary.csv')
    weather_hero = WeatherHero(data_path, output_path)
    weather_hero.process_weather_data()
    print("Success!")
    