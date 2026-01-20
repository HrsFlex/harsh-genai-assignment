import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from mobility_analytics import MobilityDataAnalyzer
from database_manager import MobilityDBManager
import os

DATASET_PATH = "yellow_tripdata_2016-01.csv"
SAMPLE_SIZE = 50000 
DB_PATH = "mobility.db"
SQL_QUERIES_FILE = "sql_queries.sql"
OUTPUT_DIR = "deliverables"

def setup_environment():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

def load_and_ingest_data():
    print("Initializing Data Analyzer...")
    path_to_use = DATASET_PATH
    if not os.path.exists(path_to_use):
        if os.path.exists("dataset_sample.csv"):
            path_to_use = "dataset_sample.csv"
            print(f"Full dataset not found. Using {path_to_use}")
        else:
            raise FileNotFoundError(f"Neither {DATASET_PATH} nor dataset_sample.csv found.")

    analyzer = MobilityDataAnalyzer(path_to_use)
    df = analyzer.load_data(nrows=SAMPLE_SIZE)
    analyzer.clean_data()
    analyzer.feature_engineering()
    
    print("Ingesting data into Database...")
    db_manager = MobilityDBManager(DB_PATH)
    db_manager.ingest_data(analyzer)
    return db_manager, analyzer.data

def run_sql_queries(db_manager):
    print("Running SQL Queries...")
    
    with open(SQL_QUERIES_FILE, 'r') as f:
        sql_content = f.read()
    
    queries = []
    current_query = []
    
    for line in sql_content.splitlines():
        line = line.strip()
        if not line or line.startswith('--'):
            continue
        current_query.append(line)
        if line.endswith(';'):
            queries.append("\n".join(current_query))
            current_query = []
            
    results_output = []
    results_output.append("SQL QUERY EXECUTION RESULTS")
    results_output.append("===========================\n")
    
    for i, query in enumerate(queries, 1):
        try:
            results_output.append(f"Query #{i}:")
            results_output.append(query)
            results_output.append("-" * 20)
            
            df_result = db_manager.run_query(query)
            results_output.append(df_result.to_string())
            results_output.append("\n" + "="*50 + "\n")
            print(f"Executed Query #{i}")
            
        except Exception as e:
            results_output.append(f"Error executing query: {e}")
            results_output.append("\n" + "="*50 + "\n")
            print(f"Error in Query #{i}: {e}")

    output_file = os.path.join(OUTPUT_DIR, "sql_results.txt")
    with open(output_file, 'w') as f:
        f.write("\n".join(results_output))
    print(f"SQL Results saved to {output_file}")

def calculate_kpis(df):
    print("Calculating Core KPIs...")
    kpi_output = []
    kpi_output.append("CORE KPI REPORT")
    kpi_output.append("===============\n")

    total_revenue = df['total_amount'].sum()
    monthly_revenue = df.groupby('pickup_month')['total_amount'].sum()
    kpi_output.append(f"1. Total Revenue: ${total_revenue:,.2f}")
    kpi_output.append("   Monthly Revenue:")
    for month, rev in monthly_revenue.items():
        kpi_output.append(f"   - Month {month}: ${rev:,.2f}")
    
    avg_distance = df['trip_distance'].mean()
    kpi_output.append(f"\n2. Average Trip Distance: {avg_distance:.2f} miles")

    avg_fare = df['fare_amount'].mean()
    kpi_output.append(f"\n3. Average Fare per Trip: ${avg_fare:.2f}")

    total_fare_for_tip = df['fare_amount'].sum()
    total_tips = df['tip_amount'].sum()
    tip_percentage = (total_tips / total_fare_for_tip) * 100 if total_fare_for_tip > 0 else 0
    kpi_output.append(f"\n4. Tip Percentage (of Fare): {tip_percentage:.2f}%")

    trips_per_hour = df.groupby('pickup_hour').size()
    peak_hour = trips_per_hour.idxmax()
    peak_trips = trips_per_hour.max()
    kpi_output.append(f"\n5. Peak Demand: Hour {peak_hour} with {peak_trips} trips")

    total_distance = df['trip_distance'].sum()
    rev_per_mile = total_revenue / total_distance if total_distance > 0 else 0
    kpi_output.append(f"\n6. Revenue per Mile: ${rev_per_mile:.2f}")

    def get_time_slot(hour):
        if (7 <= hour <= 10) or (17 <= hour <= 20):
            return 'Peak'
        return 'Off-Peak'
    
    df['time_slot'] = df['pickup_hour'].apply(get_time_slot)
    utilization = df['time_slot'].value_counts(normalize=True) * 100
    kpi_output.append("\n7. Peak vs Off-Peak Utilization:")
    for slot, pct in utilization.items():
        kpi_output.append(f"   - {slot}: {pct:.1f}% of trips")

    output_file = os.path.join(OUTPUT_DIR, "kpi_report.txt")
    with open(output_file, 'w') as f:
        f.write("\n".join(kpi_output))
    print(f"KPI Report saved to {output_file}")
    
    print("\n".join(kpi_output))

def generate_visualizations(df):
    print("Generating Requested Visualizations...")
    sns.set_theme(style="whitegrid")
    
    plt.figure(figsize=(10, 6))
    daily_rev = df.groupby('pickup_day')['total_amount'].sum().reset_index()
    sns.lineplot(data=daily_rev, x='pickup_day', y='total_amount', marker='o', color='green', linewidth=2.5)
    plt.title('Monthly Revenue Trends (Daily Breakdown)')
    plt.xlabel('Day of Month')
    plt.ylabel('Total Revenue ($)')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "viz_1_revenue_trends.png"))
    plt.close()

    plt.figure(figsize=(12, 8))
    heatmap_data = df.pivot_table(index='pickup_weekday', columns='pickup_hour', values='VendorID', aggfunc='count')
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex(days_order)
    
    sns.heatmap(heatmap_data, cmap="YlOrRd", annot=False, fmt="d")
    plt.title('Hourly Demand Heatmap (Day vs Hour)')
    plt.xlabel('Hour of Day')
    plt.ylabel('Day of Week')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "viz_2_hourly_heatmap.png"))
    plt.close()

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    sns.boxplot(y=df['fare_amount'], ax=axes[0], color='skyblue')
    axes[0].set_title('Fare Amount Distribution (Outliers)')
    axes[0].set_ylabel('Fare ($)')
    axes[0].set_ylim(0, 150) 

    sns.boxplot(y=df['trip_distance'], ax=axes[1], color='lightgreen')
    axes[1].set_title('Trip Distance Distribution (Outliers)')
    axes[1].set_ylabel('Distance (miles)')
    axes[1].set_ylim(0, 30)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "viz_3_outliers.png"))
    plt.close()

    df['time_of_day'] = pd.cut(df['pickup_hour'], 
                               bins=[0, 6, 12, 18, 24], 
                               labels=['Night', 'Morning', 'Afternoon', 'Evening'],
                               right=False)
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='time_of_day', y='tip_amount', palette="Set3")
    plt.title('Tip Distribution by Time of Day')
    plt.xlabel('Time of Day')
    plt.ylabel('Tip Amount ($)')
    plt.ylim(0, 15)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "viz_4_tip_distribution.png"))
    plt.close()
    
    print("Visualizations saved.")

if __name__ == "__main__":
    setup_environment()
    db_manager, df = load_and_ingest_data()
    run_sql_queries(db_manager)
    calculate_kpis(df)
    generate_visualizations(df)
    print("All deliverables generated.")
