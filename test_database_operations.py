"""
CST8002 - Practical Project 2
Professor: Tyler DeLay
Date: 15/05/2025
Author: Himanish Rishi

Test script to demonstrate database operations for milk sample data.
This script shows the complete CRUD operations and data migration process.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.persistence.database_config import DatabaseConfig
from src.persistence.milk_sample_db_repository import MilkSampleDBRepository
from src.persistence.data_migration import DataMigration
from src.business.milk_sample_db_service import MilkSampleDBService
from src.model.milk_sample_record import MilkSampleRecord

def test_database_creation():
    """Test database creation and table initialization."""
    print("=" * 60)
    print("STEP 1: Database Creation and Table Initialization")
    print("=" * 60)
    
    try:
        # Create database configuration
        db_config = DatabaseConfig("test_milk_samples.db")
        
        # Initialize database (creates table)
        db_config.initialize_database()
        
        print("✓ Database and table created successfully!")
        return db_config
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        return None

def test_data_migration():
    """Test data migration from CSV to database."""
    print("\n" + "=" * 60)
    print("STEP 2: Data Migration from CSV to Database")
    print("=" * 60)
    
    try:
        # Create migration utility
        migration = DataMigration()
        
        # Migrate data from CSV to database
        total, successful, failed = migration.migrate_data(batch_size=50)
        
        print(f"\nMigration Results:")
        print(f"Total records: {total}")
        print(f"Successful inserts: {successful}")
        print(f"Failed inserts: {failed}")
        
        # Verify migration
        if migration.verify_migration():
            print("✓ Data migration verified successfully!")
        else:
            print("✗ Data migration verification failed!")
            
        # Get migration statistics
        stats = migration.get_migration_statistics()
        print(f"\nMigration Statistics:")
        print(f"CSV records: {stats.get('csv_record_count', 0)}")
        print(f"Database records: {stats.get('db_record_count', 0)}")
        print(f"Unique provinces: {stats.get('unique_provinces', 0)}")
        print(f"Unique stations: {stats.get('unique_stations', 0)}")
        
        return True
    except Exception as e:
        print(f"✗ Error during data migration: {e}")
        return False

def test_create_operations():
    """Test CREATE operations."""
    print("\n" + "=" * 60)
    print("STEP 3: CREATE Operations")
    print("=" * 60)
    
    try:
        service = MilkSampleDBService()
        
        # Create a new sample record
        record_id, new_record = service.create_new_sample(
            sample_type="MILK",
            type="WHOLE",
            start_date="01-Jan-24",
            stop_date="31-Jan-24",
            station_name="TEST STATION",
            province="TEST PROVINCE",
            sr90_activity=0.05,
            sr90_error=0.01,
            sr90_activity_per_calcium=0.04
        )
        
        print(f"✓ Created new sample with ID: {record_id}")
        print(f"Sample details: {new_record}")
        
        return record_id
    except Exception as e:
        print(f"✗ Error creating sample: {e}")
        return None

def test_read_operations():
    """Test READ operations."""
    print("\n" + "=" * 60)
    print("STEP 4: READ Operations")
    print("=" * 60)
    
    try:
        service = MilkSampleDBService()
        
        # Get total count
        total_count = service.get_sample_count()
        print(f"Total samples in database: {total_count}")
        
        # Get first 5 samples
        samples = service.get_all_samples(limit=5)
        print(f"\nFirst 5 samples:")
        for i, sample in enumerate(samples, 1):
            print(f"{i}. {sample.station_name}, {sample.province} - {sample.sr90_activity} Bq/L")
        
        # Get samples by province
        provinces = service.get_available_provinces()
        if provinces:
            test_province = provinces[0]
            province_samples = service.get_samples_by_province(test_province)
            print(f"\nSamples from {test_province}: {len(province_samples)}")
        
        # Get samples by station
        stations = service.get_available_stations()
        if stations:
            test_station = stations[0]
            station_samples = service.get_samples_by_station(test_station)
            print(f"Samples from {test_station}: {len(station_samples)}")
        
        # Get statistics
        stats = service.get_statistics()
        print(f"\nDatabase Statistics:")
        print(f"Total samples: {stats['total_samples']}")
        print(f"Unique provinces: {stats['unique_provinces']}")
        print(f"Unique stations: {stats['unique_stations']}")
        print(f"Average Sr90 activity: {stats['average_sr90_activity']:.6f} Bq/L")
        
        print("✓ READ operations completed successfully!")
        return True
    except Exception as e:
        print(f"✗ Error during READ operations: {e}")
        return False

def test_update_operations(record_id):
    """Test UPDATE operations."""
    print("\n" + "=" * 60)
    print("STEP 5: UPDATE Operations")
    print("=" * 60)
    
    try:
        service = MilkSampleDBService()
        
        # Get the record before update
        original_record = service.get_sample_by_id(record_id)
        if not original_record:
            print(f"✗ Record with ID {record_id} not found")
            return False
        
        print(f"Original record: {original_record}")
        
        # Update the record
        success, old_record, updated_record = service.edit_sample(
            record_id,
            sr90_activity=0.075,
            sr90_error=0.015
        )
        
        if success:
            print(f"✓ Updated record with ID: {record_id}")
            print(f"Old Sr90 activity: {old_record.sr90_activity}")
            print(f"New Sr90 activity: {updated_record.sr90_activity}")
        else:
            print(f"✗ Failed to update record with ID: {record_id}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error during UPDATE operations: {e}")
        return False

def test_delete_operations(record_id):
    """Test DELETE operations."""
    print("\n" + "=" * 60)
    print("STEP 6: DELETE Operations")
    print("=" * 60)
    
    try:
        service = MilkSampleDBService()
        
        # Get the record before deletion
        record_to_delete = service.get_sample_by_id(record_id)
        if not record_to_delete:
            print(f"✗ Record with ID {record_id} not found")
            return False
        
        print(f"Record to delete: {record_to_delete}")
        
        # Delete the record
        success, deleted_record = service.delete_sample(record_id)
        
        if success:
            print(f"✓ Deleted record with ID: {record_id}")
            print(f"Deleted record: {deleted_record}")
            
            # Verify deletion
            verify_record = service.get_sample_by_id(record_id)
            if verify_record is None:
                print("✓ Deletion verified - record no longer exists")
            else:
                print("✗ Deletion verification failed - record still exists")
        else:
            print(f"✗ Failed to delete record with ID: {record_id}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error during DELETE operations: {e}")
        return False

def main():
    """Main test function."""
    print("Database Operations Test Suite")
    print("Testing CRUD operations for milk sample data")
    
    # Step 1: Create database
    db_config = test_database_creation()
    if not db_config:
        print("Database creation failed. Exiting.")
        return
    
    # Step 2: Migrate data
    if not test_data_migration():
        print("Data migration failed. Exiting.")
        return
    
    # Step 3: Test CREATE
    record_id = test_create_operations()
    if not record_id:
        print("CREATE operations failed. Exiting.")
        return
    
    # Step 4: Test READ
    if not test_read_operations():
        print("READ operations failed.")
    
    # Step 5: Test UPDATE
    if not test_update_operations(record_id):
        print("UPDATE operations failed.")
    
    # Step 6: Test DELETE
    if not test_delete_operations(record_id):
        print("DELETE operations failed.")
    
    print("\n" + "=" * 60)
    print("Database Operations Test Complete!")
    print("=" * 60)
    
    # Clean up test database
    try:
        db_config.drop_table()
        db_config.close_connection()
        print("✓ Test database cleaned up")
    except Exception as e:
        print(f"✗ Error cleaning up test database: {e}")

if __name__ == "__main__":
    main() 