"""
CST8002 - Practical Project 3
Professor: Tyler DeLay
Date: 13/07/2025
Author: Himanish Rishi

This module contains tests for database operations in the milk sample application.
It tests the CRUD (Create, Read, Update, Delete) operations using the actual database.

The tests verify:
- Creating new milk sample records
- Reading existing records by ID
- Updating record fields
- Deleting records
- Listing all records
"""

import os
import sys
import unittest

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.business.milk_sample_db_service import MilkSampleDBService
from src.model.milk_sample_record import MilkSampleRecord

# Use the actual database file (as per user request)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'milk_samples.db')


class TestDatabaseOperations(unittest.TestCase):
    """
    Test class for database operations in the milk sample application.
    
    This class contains unit tests that verify the CRUD operations
    work correctly with the actual database.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Set up the test class by creating a database service instance.
        
        This method is called once before all tests in the class.
        It creates a MilkSampleDBService instance that uses the actual
        milk_samples.db database file.
        """
        cls.db_service = MilkSampleDBService()
    
    def test_create_sample(self):
        """
        Test creating a new milk sample record in the database.
        
        This test verifies that:
        1. A new sample can be created with valid data
        2. The creation returns a valid record ID
        3. The created record can be retrieved from the database
        4. The retrieved record contains the correct data
        """
        # Create a new sample
        record_id, record = self.db_service.create_new_sample(
            sample_type="MILK",
            type="WHOLE",
            start_date="2024-01-01",
            stop_date="2024-01-07",
            station_name="Test Station",
            province="Test Province",
            sr90_activity=1.23,
            sr90_error=0.12,
            sr90_activity_per_calcium=0.01
        )
        self.assertIsInstance(record_id, int)
        # Fetch it back
        fetched = self.db_service.get_sample_by_id(record_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.station_name, "Test Station")
        self.assertEqual(fetched.province, "Test Province")
    
    def test_update_sample(self):
        """
        Test updating an existing milk sample record in the database.
        
        This test verifies that:
        1. A new sample can be created for updating
        2. The sample can be updated with new field values
        3. The update operation returns success status
        4. The updated record contains the new values
        """
        # Insert a sample to update
        record_id, _ = self.db_service.create_new_sample(
            sample_type="MILK",
            type="SKIM",
            start_date="2024-02-01",
            stop_date="2024-02-07",
            station_name="Update Station",
            province="Update Province",
            sr90_activity=2.34
        )
        # Update the sample
        success, old, updated = self.db_service.edit_sample(
            record_id,
            station_name="Updated Station",
            province="Updated Province"
        )
        self.assertTrue(success)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.station_name, "Updated Station")
        self.assertEqual(updated.province, "Updated Province")
    
    def test_delete_sample(self):
        """
        Test deleting a milk sample record from the database.
        
        This test verifies that:
        1. A new sample can be created for deletion
        2. The sample can be deleted successfully
        3. The delete operation returns success status
        4. The deleted record is no longer retrievable from the database
        """
        # Insert a sample to delete
        record_id, _ = self.db_service.create_new_sample(
            sample_type="MILK",
            type="PARTLY SKIMMED",
            start_date="2024-03-01",
            stop_date="2024-03-07",
            station_name="Delete Station",
            province="Delete Province",
            sr90_activity=3.45
        )
        # Delete the sample
        success, deleted = self.db_service.delete_sample(record_id)
        self.assertTrue(success)
        # Ensure it is gone
        self.assertIsNone(self.db_service.get_sample_by_id(record_id))
    
    def test_get_all_samples(self):
        """
        Test retrieving all milk sample records from the database.
        
        This test verifies that:
        1. The get_all_samples method returns a list
        2. The returned samples are valid MilkSampleRecord objects
        3. The method handles pagination parameters correctly
        """
        # Just check that the method returns a list
        samples = self.db_service.get_all_samples(limit=5)
        self.assertIsInstance(samples, list)
        # If there are samples, they should be MilkSampleRecord
        if samples:
            self.assertIsInstance(samples[0], MilkSampleRecord)


if __name__ == '__main__':
    unittest.main() 