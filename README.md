# Weather Hero

## Description
Weather Hero is a python package that displays summary statistics derived from the Australian Weather Database.

## Setup

### Module 1
This project has been setup with systems designed for a scalable and clean codebase.

Version Control - GitHub Repo
- Repository to save versions and share code across devices
- .gitignore: Insures that the data, venv, and other files are not put in the repo

Virtual Environment - venv
- Created a virtual environment that holds all necessary packages
- requirements.txt allows anyone to replicate my venv
  - pip install -r requirements.txt 
 
### Module 2
Added: describe_weather_data()
Put .py file into ./weather_hero/ subdirectory and added __init__.py file
 
### Module 3
Added WeatherLoader, WeatherAnalyzer, WeatherSaver, and WeatherHero classes to weather_hero.py 

- WeatherLoader
  - Loads weather data from a CSV file into Pandas DataFrame
- WeatherAnalyzer
  - Analyzes weather data from a Pandas DataFrame
- WeatherSaver
  - Saves the summary statistics to a CSV file.
- WeatherHero 
  - Loads, analyzes, and saves weather data summary statistics. (Using the above classes)
        
This design makes use of OOP principles such as 
- Encapsulation
- Abstraction
- Single Responsiblity Principle
- Composition
- and more!

To lean in to the metaphor in the lecture video, I made each of the program's functionalities into its own instrument, and made a WeatherHero class to compose them into an organized orchestra.

### Module 4

I added robust error handling by using try and except blocks. I made an effort to specify the exception type whenever only one type
of error was to be expected. Otherwise, I just used the generic Exception.

I added log files and integrated logging into my error handling. Entries are categorized by level and appended to the log. This occurs whenever a significant process is completed successfully, or when any error is encountered.

I added generator/iterator functionality by creating an iter_rows() function in the DataLoader. This allows the program to read rows
from the CSV in batches, making it more robust in handling larger files. 

### Module 5
I added unit testing and doctesting to ensure correct functionality.

Tested for:
- Missing files
- Wrong file types
- Corrupt files
- Accurate summary statistics
- Successful save

### Module 6
I made test cases to test the logic of:
- Filtering a dataframe based on temperature
- Mapping two variables of a dataframe together
- Reducing a column of a dataframe

As mentioned above, I used all of these functional programming techniques in this latest update.

I used these techniques to create the following charts:
- Average Rainfall on Hot vs Cold Days
- Average Windspeed by Direction
- Total Rainfall in Dataset

### Module 7
I implemeneted asynchronous and multiprocessing processes to optimize my code base. I turned the loading of the CSV into an async task so that it would run in the background and not block the main thread. I also redid how I calculated total rainfall. Instead of summing the entire dataframe, I split it up by location and then summed all those components as they came in.

Since I added no new functionality, I did not add any additional test cases. However, I did have to modify the existing ones to account for the new asyncronous behavior. After making those simple modifications, my changes were able to pass all of the tests.

### Module 8
See Google Colab

### Module 9
In this module I've converted my application into a 3-tier web application with a browser-based user interface. I created an app.py file using flask, which delivers the necessary html and css files to the client, while also managing the backend analysis and database management. I had to modify my WeatherAnalysis class slightly, making it so that instead of running plt.show(), it saves the plot to ./static/plots so that the Flask app can access it. 

#### Setup
1. Ensure File Structure Matches Diagram
joshua_levar_3270_module_9/
│
├── app.py
│
├── weather_hero/
│   ├── __init__.py
│   └──  weather_hero.py
│
├── templates/
│   ├── index.html
│   └── results.html
│
├── static/
│   ├── style.css
│   └── plots/
│       └── # The plots will be saved here on runtime
│
└── requirements.txt

2. Run app.py in project root directory
3. Open localhost:5000 in browser