# NYC Public Schools SAT Analysis

## Project Overview
Analysis of SAT performance across 375 NYC public schools to identify top performers, 
geographic patterns, and data quality issues.

## Key Findings
- **Top School:** Stuyvesant High School (Manhattan) - 2144 total SAT
- **Best Borough:** Staten Island (1439 avg) - but smallest sample (10 schools)
- **Data Quality:** 5.3% missing test participation data (20/375 schools)
- **Performance Gap:** 248 points between strongest and weakest borough leaders

## Technologies
- Python 3.13.7
- Pandas (data manipulation)
- NumPy (numerical operations)
- Matplotlib
- Seaborn

## Project Structure
```
nyc_schools_analysis/
├── analysis.py          # Main analysis script
├── schools.csv          # Dataset (from Kaggle)
├── README.md           # Project documentation
└── requirements.txt    # Dependencies
```

## How to Run
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run analysis
python analysis.py
```

## Analysis Functions
1. `load_data()` - Initial data exploration
2. `find_top_schools(n=10)` - Top N performing schools
3. `analyze_by_borough()` - Borough-level aggregation
4. `analyze_missing_data()` - Data quality assessment
5. `best_school_per_borough()` - Top school per borough
6. `visualize_top_schools()`
7. `visualize_borough_comparaison()`
8. `visualize_score_correlation()`

## Skills Demonstrated
- Data cleaning and validation
- Aggregation and grouping
- Boolean filtering
- Statistical analysis
- Professional data presentation
- Professional data visualizing

## Data Source
[Kaggle: NYC Public School Test Results](https://www.kaggle.com/datasets/beshoyatefadel/exploring-nyc-public-school-test-result-scores)

## 👤 Author
Abdessamad AMARIR - Data Analysis Portfolio Project