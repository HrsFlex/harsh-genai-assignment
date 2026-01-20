import sqlite3
import pandas as pd
import logging
from code.mobility_analytics import MobilityDataAnalyzer


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MobilityDBManager:
    """
    Manages SQLite database interactions for Mobility Analytics.
    """
    
    def __init__(self, db_path: str = "mobility.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Establishes connection to SQLite database."""
        try:

            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            logging.info(f"Connected to SQLite database at {self.db_path}")
        except Exception as e:
            logging.error(f"Error connecting to database: {e}")
            raise

    def ingest_data(self, analyzer: MobilityDataAnalyzer):
        """
        Loads cleaned data from the Analyzer into SQLite.
        """
        if analyzer.data is None:
            logging.warning("No data found in analyzer. Loading default...")
            analyzer.load_data()
            analyzer.clean_data()
            analyzer.feature_engineering()
            
        logging.info("Writing data to SQLite table 'trips'...")
        if self.conn is None:
            self.connect()
            
        analyzer.data.to_sql('trips', self.conn, if_exists='replace', index=False)
        logging.info("Data successfully written to SQLite.")

    def run_query(self, query: str):
        """Runs a raw SQL query and returns a DataFrame."""
        if self.conn is None:
            self.connect()
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            logging.error(f"Query execution failed: {e}")
            raise

    def get_top_pickup_zones(self, limit=10):
        """Returns top pickup locations by trip count."""

        query = """
        SELECT 
            ROUND(pickup_latitude, 3) as lat,
            ROUND(pickup_longitude, 3) as lon,
            COUNT(*) as trip_count,
            AVG(total_amount) as avg_revenue
        FROM trips
        GROUP BY 1, 2
        ORDER BY trip_count DESC
        LIMIT ?
        """
        if self.conn is None:
            self.connect()
        return pd.read_sql_query(query, self.conn, params=(limit,))

    def get_hourly_demand(self):
        """Returns demand per hour of day."""
        query = """
        SELECT 
            pickup_hour,
            COUNT(*) as trip_count,
            AVG(trip_distance) as avg_distance
        FROM trips
        GROUP BY pickup_hour
        ORDER BY pickup_hour
        """
        return self.run_query(query)

    def get_revenue_trends(self):
        """Returns daily revenue trends."""
        query = """
        SELECT 
            pickup_day,
            SUM(total_amount) as total_revenue,
            AVG(fare_amount) as avg_fare
        FROM trips
        GROUP BY pickup_day
        ORDER BY pickup_day
        """
        return self.run_query(query)

if __name__ == "__main__":

    db_manager = MobilityDBManager()
    

    dataset_path = "yellow_tripdata_2016-01.csv"
    analyzer = MobilityDataAnalyzer(dataset_path)
    

    analyzer.load_data(nrows=50000)
    analyzer.clean_data()
    analyzer.feature_engineering()
    
    db_manager.ingest_data(analyzer)
    
    print("\nTop Zones:")
    print(db_manager.get_top_pickup_zones())
    
    print("\nHourly Demand:")
    print(db_manager.get_hourly_demand())
