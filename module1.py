# TODO needs pydoc

import pandas as pd

data_path = 'data/Weather Test Data.csv'
 
df = pd.read_csv(data_path)
print(df.head())


if __name__ == "__main__":
    print("Module1 executed as the main program")