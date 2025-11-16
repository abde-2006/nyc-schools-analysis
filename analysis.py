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

def find_top_schools(n=10):
    df['total_sat'] = df['average_math'] + df['average_reading'] + df['average_writing']

    sort_df = df.sort_values('total_sat', ascending=False).reset_index(drop=True)

    columns = ['school_name', 'borough', 'average_math', 'average_reading', 'average_writing', 'total_sat']
    top_n = sort_df.head(n)[columns]
    top_n.index = top_n.index + 1

    print(f"\nTop {n} Schools by SAT Score:")
    print("="*127)
    print(top_n)
    print("="*127)

    return top_n

if __name__ == "__main__":
    load_data()
    find_top_schools()