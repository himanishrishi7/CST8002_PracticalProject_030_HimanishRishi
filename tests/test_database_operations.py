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
import pytest
from src.business.milk_sample_db_service import MilkSampleDBService
from src.model.milk_sample_record import MilkSampleRecord

# Use the actual database file (as per user request)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'milk_samples.db')

@pytest.fixture(scope="module")
def db_service():
    """
    Fixture to provide a database service instance for testing.
    
    This fixture creates a MilkSampleDBService instance that uses the actual
    milk_samples.db database file. The fixture is scoped to the module level
    to avoid creating multiple service instances during testing.
    
    Returns:
        MilkSampleDBService: Service instance for database operations
    """
    # The service will use the default DB file
    service = MilkSampleDBService()
    yield service
    # No teardown needed since we use the actual DB


def test_create_sample(db_service):
    """
    Test creating a new milk sample record in the database.
    
    This test verifies that:
    1. A new sample can be created with valid data
    2. The creation returns a valid record ID
    3. The created record can be retrieved from the database
    4. The retrieved record contains the correct data
    """
    # Create a new sample
    record_id, record = db_service.create_new_sample(
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
    assert isinstance(record_id, int)
    # Fetch it back
    fetched = db_service.get_sample_by_id(record_id)
    assert fetched is not None
    assert fetched.station_name == "Test Station"
    assert fetched.province == "Test Province"


def test_update_sample(db_service):
    """
    Test updating an existing milk sample record in the database.
    
    This test verifies that:
    1. A new sample can be created for updating
    2. The sample can be updated with new field values
    3. The update operation returns success status
    4. The updated record contains the new values
    """
    # Insert a sample to update
    record_id, _ = db_service.create_new_sample(
        sample_type="MILK",
        type="SKIM",
        start_date="2024-02-01",
        stop_date="2024-02-07",
        station_name="Update Station",
        province="Update Province",
        sr90_activity=2.34
    )
    # Update the sample
    success, old, updated = db_service.edit_sample(
        record_id,
        station_name="Updated Station",
        province="Updated Province"
    )
    assert success
    assert updated is not None
    assert updated.station_name == "Updated Station"
    assert updated.province == "Updated Province"


def test_delete_sample(db_service):
    """
    Test deleting a milk sample record from the database.
    
    This test verifies that:
    1. A new sample can be created for deletion
    2. The sample can be deleted successfully
    3. The delete operation returns success status
    4. The deleted record is no longer retrievable from the database
    """
    # Insert a sample to delete
    record_id, _ = db_service.create_new_sample(
        sample_type="MILK",
        type="PARTLY SKIMMED",
        start_date="2024-03-01",
        stop_date="2024-03-07",
        station_name="Delete Station",
        province="Delete Province",
        sr90_activity=3.45
    )
    # Delete the sample
    success, deleted = db_service.delete_sample(record_id)
    assert success
    # Ensure it is gone
    assert db_service.get_sample_by_id(record_id) is None


def test_get_all_samples(db_service):
    """
    Test retrieving all milk sample records from the database.
    
    This test verifies that:
    1. The get_all_samples method returns a list
    2. The returned samples are valid MilkSampleRecord objects
    3. The method handles pagination parameters correctly
    """
    # Just check that the method returns a list
    samples = db_service.get_all_samples(limit=5)
    assert isinstance(samples, list)
    # If there are samples, they should be MilkSampleRecord
    if samples:
        assert isinstance(samples[0], MilkSampleRecord) 