import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

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
    print("\n" + "="*100)
    print("TOP SCHOOL PER BOROUGH ANALYSIS".center(100))
    print("="*100)

    idx = df.groupby('borough')['total_sat'].idxmax()

    columns = ['school_name', 'borough', 'average_math', 'average_reading', 'average_writing', 'total_sat']
    best_schools = df.loc[idx][columns].sort_values('total_sat', ascending=False)

    print("\n" + best_schools.to_string())

    print("\n" + "-"*100)
    print("KEY INSIGHTS".center(100))
    print("-"*100)

    top_school = best_schools.iloc[0]
    bottom_school = best_schools.iloc[-1]
    gap = top_school['total_sat'] - bottom_school['total_sat']

    print(f"Overall Leader: {top_school['school_name']} ({top_school['borough']})")
    print(f"   Total SAT: {top_school['total_sat']:.0f} points")
    print(f"\nPerformance Gap: {gap:.0f} points between strongest and weakest borough leader")
    print(f"   ({top_school['borough']}: {top_school['total_sat']:.0f} vs "
          f"{bottom_school['borough']}: {bottom_school['total_sat']:.0f})")
    
    print(f"\nSubject Strength Pattern:")
    for idx, row in best_schools.iterrows():
        strongest_subject = 'Math' if row['average_math'] >= max(row['average_reading'], row['average_writing']) else 'Reading/Writing'
        print(f"   {row['borough']:15s}: {strongest_subject} ({row['average_math']:.0f}M / {row['average_reading']:.0f}R / {row['average_writing']:.0f}W)")
    
    print("="*100)
    
    return best_schools

def visualize_top_schools():
    # Get data
    top_10 = find_top_schools(n=10)

    fig, ax = plt.subplots(figsize=(12, 8))

    x_values = top_10['total_sat'] 
    y_values = top_10['school_name']

    colors = plt.cm.RdYlGn(np.linspace(0.5, 0.9, len(y_values)))
    
    bars = ax.barh(y_values, x_values, color=colors, edgecolor='black', linewidth=0.7)

    for i, (bar, score) in enumerate(zip(bars, x_values)):
        ax.text(score - 50, i, f'{score:.0f}', 
                va='center', ha='right', fontsize=10, 
                fontweight='bold', color='white')

    ax.set_title('Top 10 NYC Schools by SAT Score', fontsize=18, fontweight='bold', color='#2C3E50')
    ax.set_xlabel('Total SAT score', fontsize=13, fontweight='bold', color='#34495E')
    ax.set_ylabel('School Name', fontsize=13, fontweight='bold', color='#34495E')

    ax.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.set_xlim(1800, max(x_values) + 100)
    ax.tick_params(axis='both', labelsize=11)
    ax.set_facecolor('#F8F9FA')

    plt.tight_layout()
    plt.savefig('top_schools_enhanced.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print("\nVisualization saved as 'top_schools_enhanced.png'")
    plt.show()

def visualize_borough_comparaison():
    result = analyze_by_borough()

    boroughs = result.index
    math_scores = result['avg_math']
    reading_scores = result['avg_reading']
    writing_scores = result['avg_writing']

    x = np.arange(len(boroughs))
    width = .25

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(14, 8))

    bars1 = ax.bar(x - width, math_scores, width, 
                   label='Math', color='#3498D8', edgecolor='black', linewidth=.7)
    bars2 = ax.bar(x, reading_scores, width,
                   label='Reading', color='#E74C3C', edgecolor='black', linewidth=.7)
    bars3 = ax.bar(x + width, writing_scores, width,
                   label='Writing', color='#2ECC71', edgecolor='black', linewidth=.7)

    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, 
                    f'{height:.0f}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

    add_value_labels(bars1)
    add_value_labels(bars2)
    add_value_labels(bars3)

    ax.set_xlabel('Borough', fontsize=14, fontweight='bold', color='#2C3E50')
    ax.set_ylabel('Average SAT Score', fontsize=14, fontweight='bold', color='#2C3E50')
    ax.set_title('NYC Borough Performance: Math vs Reading vs Writing\nAverage SAT Scores by Subject', 
                 fontsize=17, fontweight='bold', pad=20, color='#2C3E50')
    ax.set_xticks(x)
    ax.set_xticklabels(boroughs, fontsize=12)
    ax.tick_params(axis='y', labelsize=11)

    ax.legend(loc='upper right', fontsize=12, framealpha=0.9, edgecolor='black')

    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.7)
    ax.set_axisbelow(True)

    ax.set_ylim(380, 500)

    ax.set_facecolor('#F8F9FA')

    best_borough = boroughs[0]
    worst_borough = boroughs[-1]
    gap = math_scores.iloc[0] - math_scores.iloc[-1]

    ax.text(0.2, 0.98, f'Key Insight:\n'
                        f'• {best_borough} leads in all subjects\n'
                        f'• {worst_borough} trails by {gap:.0f} points in Math\n'
                        f'• Math scores consistently highest',
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', 
            facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    plt.savefig('borough_comparaison.png', dpi=300, bbox_inches='tight')
    print("\nEnhanced borough comparison saved as 'borough_comparison.png'")
    plt.show()

def visualize_score_correlation():
    score_cols = ['average_math', 'average_reading', 'average_writing']
    corr_matrix = df[score_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))

    sb.heatmap(
        corr_matrix,
        annot=True,         # Show correlation values
        fmt=".2f",          # Format for the annotations
        cmap='coolwarm',
        vmin=.9,            # Set minimum value for color scale
        vmax=1.0,           # Set maximum value for color scale
        center=.95,         # Center of color scale
        linewidths=2,
        square=True,
        linecolor='white',  # White borders
        cbar_kws={
            'shrink': .8,
            'label': 'Correlation Coefficient',
        },
        annot_kws={
            'size': 14,
            'weight': 'bold',
        }
    )

    plt.title("Correlation between SAT Subject Scores\nAll NYC Public Schools",
              fontsize=16, fontweight='bold', pad=20)

    ax.set_xticklabels(['Math', 'Reading', 'Writing'], fontsize=12)
    ax.set_yticklabels(['Math', 'Reading', 'Writing'], fontsize=12, rotation=0)

    insights_text = (
        "Key Findings:\n"
        f"• Reading & Writing: {corr_matrix.loc['average_reading', 'average_writing']:.2f} correlation (strongest)\n"
        f"• Math & Reading: {corr_matrix.loc['average_math', 'average_reading']:.2f} correlation\n"
        f"• Math & Writing: {corr_matrix.loc['average_math', 'average_writing']:.2f} correlation\n"
        "\n"
        "Interpretation: High correlations across all subjects\n"
        "suggest school quality is holistic, not subject-specific."
    )

    plt.text(4, 1.5, insights_text, fontsize=10,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
             verticalalignment='top')

    plt.tight_layout()
    plt.savefig('correlation_heatmap_enhanced.png', dpi=300, bbox_inches='tight')
    print("\nCorrelation heatmap saved as 'correlation_heatmap_enhanced.png'")
    plt.show()

    print("\n" + "="*70)
    print("CORRELATION ANALYSIS SUMMARY".center(70))
    print("="*70)
    print(f"\nStrongest Correlation: Reading ↔ Writing ({corr_matrix.loc['average_reading', 'average_writing']:.3f})")
    print(f"Weakest Correlation: Math ↔ Reading ({corr_matrix.loc['average_math', 'average_reading']:.3f})")
    print(f"\nAverage Correlation: {corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].mean():.3f}")
    print("\nConclusion: All SAT subjects are HIGHLY correlated (>0.90).")
    print("Schools strong in one subject tend to be strong in all subjects.")
    print("="*70)

if __name__ == "__main__":
    load_data()
    find_top_schools()
    analyze_by_borough()
    analyze_missing_data()
    best_school_per_borough()
    visualize_top_schools()
    visualize_borough_comparaison()
    visualize_score_correlation()