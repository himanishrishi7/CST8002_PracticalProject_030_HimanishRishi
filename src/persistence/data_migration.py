"""
CST8002 - Practical Project 2
Professor: Tyler DeLay
Date: 15/05/2025
Author: Himanish Rishi

This module contains the DataMigration class which handles migrating data
from the CSV file to the database. It is part of the Persistence Layer.

This module is responsible for:
- Reading the original CSV file
- Converting CSV data to database records
- Populating the database with all sample data
- Providing migration status and statistics
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import csv
from typing import List, Tuple
from src.model.milk_sample_record import MilkSampleRecord
from src.persistence.database_config import DatabaseConfig
from src.persistence.milk_sample_db_repository import MilkSampleDBRepository

class DataMigration:
    """
    A class to handle data migration from CSV to database.
    
    This class is responsible for:
    1. Reading the original CSV file
    2. Converting CSV rows to MilkSampleRecord objects
    3. Inserting records into the database
    4. Providing migration statistics
    5. Error handling during migration
    """
    
    def __init__(self, csv_filename: str = "nms_strontium90_milk_ssn_strontium90_lait.csv"):
        """
        Initialize the data migration utility.
        
        Args:
            csv_filename (str): Name of the CSV file to migrate
        """
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.csv_path = os.path.join(current_dir, csv_filename)
        self.db_repository = MilkSampleDBRepository()
        
    def read_csv_data(self) -> List[MilkSampleRecord]:
        """
        Read all data from the CSV file and convert to MilkSampleRecord objects.
        
        Returns:
            List[MilkSampleRecord]: List of all milk sample records from CSV
            
        Raises:
            FileNotFoundError: If the CSV file is not found
            ValueError: If there's an error parsing the data
        """
        records = []
        skipped_rows = 0
        total_rows = 0
        
        try:
            with open(self.csv_path, "r", encoding="utf-8-sig", errors='ignore') as f:
                csv_reader = csv.reader(f)
                next(csv_reader)  # Skip header
                
                for row_num, values in enumerate(csv_reader, start=2):
                    total_rows += 1
                    
                    try:
                        # Clean and validate values
                        cleaned_values = [v.strip() for v in values if v.strip()]
                        
                        if len(cleaned_values) < 9:
                            print(f"Skipping row {row_num}: Insufficient values (found {len(cleaned_values)}, need 9)")
                            skipped_rows += 1
                            continue
                            
                        record = MilkSampleRecord(
                            sample_type=cleaned_values[0],
                            type=cleaned_values[1],
                            start_date=cleaned_values[2],
                            stop_date=cleaned_values[3],
                            station_name=cleaned_values[4],
                            province=cleaned_values[5],
                            sr90_activity=cleaned_values[6],
                            sr90_error=cleaned_values[7],
                            sr90_activity_per_calcium=cleaned_values[8]
                        )
                        records.append(record)
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing row {row_num}: {str(e)}")
                        skipped_rows += 1
                        continue
                        
        except FileNotFoundError:
            print(f"Error: File '{self.csv_path}' not found.")
            print(f"Current working directory: {os.getcwd()}")
            print("Directory contents:")
            for file in os.listdir(os.getcwd()):
                print(f"  - {file}")
            raise
        except Exception as e:
            print(f"Unexpected error reading CSV file: {str(e)}")
            raise
            
        print(f"\nCSV File Statistics:")
        print(f"Total rows processed: {total_rows}")
        print(f"Rows skipped: {skipped_rows}")
        print(f"Rows successfully parsed: {len(records)}")
        
        return records
    
    def migrate_data(self, batch_size: int = 100) -> Tuple[int, int, int]:
        """
        Migrate all data from CSV to database.
        
        Args:
            batch_size (int): Number of records to insert in each batch
            
        Returns:
            Tuple[int, int, int]: (total_records, successful_inserts, failed_inserts)
            
        Raises:
            FileNotFoundError: If the CSV file is not found
            sqlite3.Error: If there's an error inserting into database
        """
        print("Starting data migration from CSV to database...")
        
        # Clear existing data
        print("Clearing existing database records...")
        self.db_repository.clear_all_samples()
        
        # Read CSV data
        print("Reading CSV data...")
        records = self.read_csv_data()
        total_records = len(records)
        
        if total_records == 0:
            print("No records found in CSV file. Migration aborted.")
            return 0, 0, 0
        
        # Insert records in batches
        successful_inserts = 0
        failed_inserts = 0
        
        print(f"Inserting {total_records} records into database in batches of {batch_size}...")
        
        for i in range(0, total_records, batch_size):
            batch = records[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_records + batch_size - 1) // batch_size
            
            print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} records)...")
            
            for record in batch:
                try:
                    self.db_repository.create_sample(record)
                    successful_inserts += 1
                except Exception as e:
                    print(f"Failed to insert record: {str(e)}")
                    failed_inserts += 1
        
        print(f"\nMigration completed!")
        print(f"Total records processed: {total_records}")
        print(f"Successful inserts: {successful_inserts}")
        print(f"Failed inserts: {failed_inserts}")
        
        # Verify migration
        db_count = self.db_repository.get_sample_count()
        print(f"Records in database: {db_count}")
        
        if db_count == successful_inserts:
            print("✓ Migration verification successful!")
        else:
            print("⚠ Migration verification failed - record count mismatch!")
        
        return total_records, successful_inserts, failed_inserts
    
    def verify_migration(self) -> bool:
        """
        Verify that the migration was successful by comparing record counts.
        
        Returns:
            bool: True if migration is verified, False otherwise
        """
        try:
            # Count records in CSV
            csv_records = self.read_csv_data()
            csv_count = len(csv_records)
            
            # Count records in database
            db_count = self.db_repository.get_sample_count()
            
            print(f"\nMigration Verification:")
            print(f"Records in CSV: {csv_count}")
            print(f"Records in database: {db_count}")
            
            if csv_count == db_count:
                print("✓ Migration verification successful!")
                return True
            else:
                print("⚠ Migration verification failed - record count mismatch!")
                return False
                
        except Exception as e:
            print(f"Error during migration verification: {str(e)}")
            return False
    
    def get_migration_statistics(self) -> dict:
        """
        Get comprehensive migration statistics.
        
        Returns:
            dict: Dictionary containing migration statistics
        """
        try:
            csv_records = self.read_csv_data()
            db_count = self.db_repository.get_sample_count()
            
            # Get unique provinces and stations from database
            provinces = set()
            stations = set()
            
            all_db_records = self.db_repository.read_all_samples()
            for record in all_db_records:
                provinces.add(record.province)
                stations.add(record.station_name)
            
            stats = {
                'csv_record_count': len(csv_records),
                'db_record_count': db_count,
                'unique_provinces': len(provinces),
                'unique_stations': len(stations),
                'provinces': sorted(list(provinces)),
                'stations': sorted(list(stations)),
                'migration_successful': len(csv_records) == db_count
            }
            
            return stats
            
        except Exception as e:
            print(f"Error getting migration statistics: {str(e)}")
            return {} 