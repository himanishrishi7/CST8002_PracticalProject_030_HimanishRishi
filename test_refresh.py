"""
Test script to debug database refresh functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.persistence.database_config import DatabaseConfig
from src.persistence.milk_sample_db_repository import MilkSampleDBRepository
from src.persistence.data_migration import DataMigration

def test_refresh():
    """Test the database refresh functionality."""
    print("=" * 60)
    print("Testing Database Refresh")
    print("=" * 60)
    
    try:
        # Step 1: Check initial state
        print("Step 1: Checking initial database state...")
        db_config = DatabaseConfig()
        repo = MilkSampleDBRepository(db_config)
        
        initial_count = repo.get_sample_count()
        print(f"Initial record count: {initial_count}")
        
        # Step 2: Clear the database
        print("\nStep 2: Clearing database...")
        cleared_count = repo.clear_all_samples()
        print(f"Cleared {cleared_count} records")
        
        # Step 3: Check if database is empty
        print("\nStep 3: Checking if database is empty...")
        empty_count = repo.get_sample_count()
        print(f"Records after clearing: {empty_count}")
        
        # Step 4: Reload data
        print("\nStep 4: Reloading data from CSV...")
        migration = DataMigration()
        total, successful, failed = migration.migrate_data()
        print(f"Migration results: {successful} successful, {failed} failed")
        
        # Step 5: Check final state
        print("\nStep 5: Checking final database state...")
        final_count = repo.get_sample_count()
        print(f"Final record count: {final_count}")
        
        # Step 6: Test with a few sample IDs
        print("\nStep 6: Testing sample retrieval...")
        for test_id in [1, 2, 3]:
            sample = repo.read_sample_by_id(test_id)
            if sample:
                print(f"✓ Found sample ID {test_id}: {sample.station_name}")
            else:
                print(f"✗ Sample ID {test_id} not found")
        
        return True
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_refresh()
    if success:
        print("\n✓ Refresh test completed successfully!")
    else:
        print("\n✗ Refresh test failed!") 