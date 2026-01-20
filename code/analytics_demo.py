

import pandas as pd
import numpy as np
from code.mobility_analytics import MobilityDataAnalyzer
from code.database_manager import MobilityDBManager
from code.genai_assistant import GenAIAssistant

def main():
    print("=" * 60)
    print("🚕 Urban Mobility Analytics - Demo Script")
    print("=" * 60)
    

    dataset_path = "yellow_tripdata_2016-01.csv"
    
    analyzer = MobilityDataAnalyzer(dataset_path)
    analyzer.load_data(nrows=10000)  # Use smaller sample for demo
    analyzer.clean_data()
    analyzer.feature_engineering()
    
    print(f"   ✅ Loaded {len(analyzer.data):,} records")
    print(f"   ✅ Columns: {list(analyzer.data.columns)[:5]}...")
    

    df = analyzer.data
    print(f"   💰 Total Revenue: ${df['total_amount'].sum():,.2f}")
    print(f"   🚕 Total Trips: {len(df):,}")
    print(f"   💵 Average Fare: ${df['fare_amount'].mean():.2f}")
    print(f"   📍 Average Distance: {df['trip_distance'].mean():.2f} miles")
    

    db = MobilityDBManager()
    db.ingest_data(analyzer)
    

    hourly = db.get_hourly_demand()
    peak_hour = hourly.loc[hourly['trip_count'].idxmax(), 'pickup_hour']
    print(f"   🕐 Peak Hour: {int(peak_hour)}:00")
    

    daily = db.get_revenue_trends()
    best_day = daily.loc[daily['total_revenue'].idxmax(), 'pickup_day']
    print(f"   📅 Best Revenue Day: Day {int(best_day)}")
    

    ai = GenAIAssistant()
    print(f"   Provider: {ai.provider}")
    print(f"   Mode: {ai.mode}")
    
    if ai.mode == "live":
        print("\n   💬 Testing AI Query...")
        insight = ai.generate_insight("Sample taxi data", "What's the revenue trend?")
        print(f"   Response: {insight[:150]}...")
    
    print("\n" + "=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
