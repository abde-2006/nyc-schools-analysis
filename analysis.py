import numpy as np
import pandas as pd

df = pd.read_csv('schools.csv')

def load_data():
    print("First 5 rows:")
    print(df.head())

    print("\nDataSet Info:")
    print(df.info())

    print("\nStatistical Summary:")
    print(df.describe())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nColumns Names:")
    print(df.columns.tolist())

if __name__ == "__main__":
    load_data()