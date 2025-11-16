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

def analyze_by_borough():
    result = df.groupby('borough').agg({
        'average_math': 'mean',
        'average_reading': 'mean',
        'average_writing': 'mean',
        'total_sat': 'mean',
        'school_name': 'count'
    }).round(2)

    result.columns = ['avg_math', 'avg_reading', 'avg_writing', 'avg_total_sat', 'num_schools']

    result = result.sort_values('avg_total_sat', ascending=False)

    print("\n" + "="*90)
    print("BOROUGH PERFORMANCE ANALYSIS".center(90))
    print("="*90)
    print(result.to_string())
    print("="*90)
    print(f"Key Insight: {result.index[0]} leads with {result.iloc[0]['avg_total_sat']:.0f} avg SAT")
    print(f"Based on {result.iloc[0]['num_schools']:.0f} schools")
    print("="*90)

    return result

def analyze_missing_data():
    missing_df = df[df['percent_tested'].isnull()]

    columns = ['school_name', 'borough', 'total_sat']
    print(missing_df[columns])

    borough_counts = missing_df.groupby('borough').size()
    print("\nCount of missing percent_tested by borough:")
    print(borough_counts)
    
    print("\nSAT score summary for schools with missing percent_tested:")
    print(missing_df['total_sat'].describe().apply(lambda x: f"{x:.2f}"))
    
if __name__ == "__main__":
    load_data()
    find_top_schools()
    analyze_by_borough()
    analyze_missing_data()