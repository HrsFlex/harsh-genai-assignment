import pandas as pd
import numpy as np
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MobilityDataAnalyzer:
    """
    A class to handle loading, cleaning, and feature engineering of NYC Taxi Trip data.
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        
    def load_data(self, nrows: int = None):
        """
        Loads the dataset from CSV.
        
        Args:
            nrows (int, optional): Number of rows to read. Useful for testing.
        """
        logging.info(f"Loading data from {self.file_path}...")
        try:

            dtype_map = {
                'VendorID': 'int8',
                'passenger_count': 'int8',
                'RatecodeID': 'int8',
                'payment_type': 'int8',
                'trip_distance': 'float32',
                'pickup_longitude': 'float32',
                'pickup_latitude': 'float32',
                'dropoff_longitude': 'float32',
                'dropoff_latitude': 'float32',
                'fare_amount': 'float32',
                'extra': 'float32',
                'mta_tax': 'float32',
                'tip_amount': 'float32',
                'tolls_amount': 'float32',
                'improvement_surcharge': 'float32',
                'total_amount': 'float32'
            }
            
            self.data = pd.read_csv(self.file_path, nrows=nrows)
            

            logging.info("Converting datetime columns...")
            self.data['tpep_pickup_datetime'] = pd.to_datetime(self.data['tpep_pickup_datetime'])
            self.data['tpep_dropoff_datetime'] = pd.to_datetime(self.data['tpep_dropoff_datetime'])
            
            logging.info(f"Successfully loaded {len(self.data)} rows.")
            return self.data
            
        except FileNotFoundError:
            logging.error(f"File not found at {self.file_path}")
            raise
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise

    def clean_data(self):
        """
        Cleans the dataset:
        1. Removes field with 0 passenger count.
        2. Removes trips with 0 distance.
        3. Removes trips with 0 or negative fares.
        4. Filters out invalid coordinates (bounding box for NYC).
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        logging.info("Starting data cleaning...")
        initial_count = len(self.data)
        

        

        

        

        self.data = self.data[
            (self.data['pickup_latitude'].between(40.5, 40.95)) &
            (self.data['pickup_longitude'].between(-74.25, -73.7)) &
            (self.data['dropoff_latitude'].between(40.5, 40.95)) &
            (self.data['dropoff_longitude'].between(-74.25, -73.7))
        ]
        
        cleaned_count = len(self.data)
        logging.info(f"Data cleaning complete. Removed {initial_count - cleaned_count} rows. Remaining: {cleaned_count}")
        return self.data

    def feature_engineering(self):
        """
        Adds derived features:
        - Hour, Day, Month, Weekday
        - Trip Duration (minutes)
        """
        if self.data is None:
            raise ValueError("Data not loaded or empty.")
            
        logging.info("Starting feature engineering...")
        

        self.data['pickup_hour'] = self.data['tpep_pickup_datetime'].dt.hour
        self.data['pickup_day'] = self.data['tpep_pickup_datetime'].dt.day
        self.data['pickup_month'] = self.data['tpep_pickup_datetime'].dt.month
        self.data['pickup_weekday'] = self.data['tpep_pickup_datetime'].dt.day_name()
        

        self.data['trip_duration_min'] = (self.data['tpep_dropoff_datetime'] - self.data['tpep_pickup_datetime']).dt.total_seconds() / 60.0

        self.data = self.data[(self.data['trip_duration_min'] > 0) & (self.data['trip_duration_min'] < 600)]
        
        logging.info("Feature engineering complete.")
        return self.data

if __name__ == "__main__":

    dataset_path = "yellow_tripdata_2016-01.csv"
    analyzer = MobilityDataAnalyzer(dataset_path)
    

    df = analyzer.load_data(nrows=100000)
    print("Initial columns:", df.columns)
    
    df = analyzer.clean_data()
    df = analyzer.feature_engineering()
    
    print("\nProcessed Data Head:")
    print(df[['tpep_pickup_datetime', 'trip_distance', 'total_amount', 'pickup_hour', 'trip_duration_min']].head())
    print("\nData Info:")
    print(df.info())
