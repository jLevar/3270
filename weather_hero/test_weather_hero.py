import os
import tempfile
import unittest
from weather_hero import WeatherLoader, WeatherSaver, WeatherAnalyzer, WeatherHero
import pandas as pd

class TestWeatherHero(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.test_file = os.path.join(base_dir, "data", "test.csv")
        self.loader = WeatherLoader(self.test_file)
    
    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            wl = WeatherLoader("data/fake.csv")
            wl.load_weather_data()

    def test_non_csv_file(self):
        with self.assertRaises(ValueError):
            wl = WeatherLoader("data/words.txt")
            wl.load_weather_data()

    def test_bad_csv_file(self):    
        with self.assertRaises(pd.errors.ParserError):
            wl = WeatherLoader("data/corrupt.csv")
            wl.load_weather_data()

        with self.assertRaises(pd.errors.ParserError):
            wl = WeatherLoader("data/corrupt.csv")
            [row for row in wl.iter_rows()]

    def test_accurate_summary(self):
        df = pd.DataFrame({
            "temp": [10, 20, 30],        
            "humidity": [50, 50, 70],     
            "condition": ["sunny", "rainy", "sunny"],  
            "city": ["A", "B", "C"]       
        })
        wa = WeatherAnalyzer(df)
        summary_df = wa.generate_summary_statistics()

        self.assertEqual(summary_df["numerical"].loc["temp"]["mean"], 20)
        self.assertEqual(summary_df["numerical"].loc["humidity"]["median"], 50)
        self.assertEqual(summary_df["categorical"].loc["top"]["condition"], "sunny")
        self.assertEqual(summary_df["categorical"].loc["count"]["city"], 3)


    def test_save(self):
        wl = WeatherLoader("data/test.csv")
        wa = WeatherAnalyzer(wl.load_weather_data())
        summary_df = wa.generate_summary_statistics()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "summary.csv")
            ws = WeatherSaver(file_path)
            ws.save_summary(summary_df)
            assert os.path.exists(file_path)


if __name__ == '__main__':
    print("Starting tests")
    unittest.main()