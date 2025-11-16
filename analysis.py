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

    print("\n" + "="*90)
    print("MISSING DATA ANALYSIS".center(90))
    print("="*90)

    print(f"\n{len(missing_df)} schools are missing 'percent_tested' data:\n")
    display_cols = ['school_name', 'borough', 'total_sat']
    print(missing_df[display_cols].to_string(index=False))

    print("\n" + "-"*90)
    print("DISTRIBUTION BY BOROUGH".center(90))
    print("-"*90)
    borough_counts = missing_df.groupby('borough').size().sort_values(ascending=False)
    for borough, count in borough_counts.items():
        percentage = (count / len(missing_df)) * 100
        print(f"{borough:15s}: {count:2d} schools ({percentage:5.1f}%)")

    print("\n" + "-"*90)
    print("SAT PERFORMANCE SUMMARY".center(90))
    print("-"*90)
    stats = missing_df['total_sat'].describe()
    
    print(f"Count:      {stats['count']:6.0f} schools")
    print(f"Mean:       {stats['mean']:6.2f}")
    print(f"Std Dev:    {stats['std']:6.2f}")
    print(f"Min:        {stats['min']:6.2f}")
    print(f"25%:        {stats['25%']:6.2f}")
    print(f"Median:     {stats['50%']:6.2f}")
    print(f"75%:        {stats['75%']:6.2f}")
    print(f"Max:        {stats['max']:6.2f}")
    
    print("\n" + "-"*90)
    print("KEY INSIGHTS".center(90))
    print("-"*90)
    overall_mean = df['total_sat'].mean()
    print(f"• Missing data affects {len(missing_df)}/{len(df)} schools ({len(missing_df)/len(df)*100:.1f}%)")
    print(f"• Average SAT for schools with missing data: {stats['mean']:.0f}")
    print(f"• Overall average SAT: {overall_mean:.0f}")
    print(f"• Difference: {stats['mean'] - overall_mean:+.0f} points")
    
    if abs(stats['mean'] - overall_mean) < 50:
        print("• Missing data appears RANDOM (no performance bias detected)")
    else:
        print("• Missing data may be SYSTEMATIC (performance-related pattern)")
    
    print("="*90)
    
    return missing_df

def best_school_per_borough():
    print("\n")
    print("="*90)
    print("BEST SCHOOL PER BOROUGH:".center(90))
    print("="*90)

    idx = df.groupby('borough')['total_sat'].idxmax()
    print("\n", idx)

    columns = ['school_name', 'borough', 'average_math', 'average_reading', 'average_writing', 'total_sat']
    best_schools = df.loc[idx][columns].sort_values('total_sat', ascending=False)
    print("\n", best_schools)



if __name__ == "__main__":
    load_data()
    find_top_schools()
    analyze_by_borough()
    analyze_missing_data()
    best_school_per_borough()