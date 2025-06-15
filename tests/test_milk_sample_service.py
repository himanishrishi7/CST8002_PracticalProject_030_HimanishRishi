"""
CST8002 - Practical Project 2
Professor: Tyler DeLay
Due Date: 25/05/2025
Author: Himanish Rishi

This module contains unit tests for the MilkSampleService class.

The tests verify the functionality of the service layer, ensuring that:
- Records can be created and stored correctly
- Data validation works as expected
- The in-memory collection is properly maintained
- All operations return expected results

Test Structure:
- Each test method focuses on a specific functionality
- Tests use the Arrange-Act-Assert pattern
- Test data is isolated and independent
- Clean state is maintained between tests
"""

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.business.milk_sample_service import MilkSampleService
from src.business.milk_sample_record import MilkSampleRecord

class TestMilkSampleService(unittest.TestCase):
    """
    Test cases for the MilkSampleService class.
    
    This test class verifies the functionality of the MilkSampleService,
    focusing on the record creation and management operations. Each test
    method is independent and tests a specific aspect of the service.
    
    Test Methods:
        - test_create_new_sample: Verifies record creation functionality
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        
        This method runs before each test to ensure a clean state.
        It creates a new service instance and clears any existing samples.
        This ensures that tests are independent and don't affect each other.
        """
        self.service = MilkSampleService()
        # Clear existing samples to start with a clean state
        self.service.samples.clear()
    
    def test_create_new_sample(self):
        """
        Test creating a new milk sample record.
        
        This test verifies that:
        1. A new record can be created with valid data
        2. The record is correctly added to the collection
        3. All fields are properly stored
        4. The returned record matches the input data
        
        Test Steps:
        1. Arrange: Set up test data and initial state
        2. Act: Call the create_new_sample method
        3. Assert: Verify the results
        
        Test Data:
            - Complete record with all fields
            - Realistic values matching expected format
        
        Assertions:
            - Collection size increases by 1
            - Returned record is of correct type
            - All fields match input data
            - Stored record matches input data
        """
        # Arrange
        initial_count = len(self.service.samples)
        test_data = {
            'sample_type': 'MILK',
            'type': 'WHOLE',
            'start_date': '2024-01-01',
            'stop_date': '2024-01-31',
            'station_name': 'Test Station',
            'province': 'Test Province',
            'sr90_activity': 0.5,
            'sr90_error': 0.1,
            'sr90_activity_per_calcium': 0.2
        }
        
        # Act
        new_sample = self.service.create_new_sample(**test_data)
        
        # Assert
        # Check if the sample was added to the collection
        self.assertEqual(len(self.service.samples), initial_count + 1)
        
        # Check if the returned sample matches the input data
        self.assertIsInstance(new_sample, MilkSampleRecord)
        self.assertEqual(new_sample.sample_type, test_data['sample_type'])
        self.assertEqual(new_sample.type, test_data['type'])
        self.assertEqual(new_sample.start_date, test_data['start_date'])
        self.assertEqual(new_sample.stop_date, test_data['stop_date'])
        self.assertEqual(new_sample.station_name, test_data['station_name'])
        self.assertEqual(new_sample.province, test_data['province'])
        self.assertEqual(new_sample.sr90_activity, test_data['sr90_activity'])
        self.assertEqual(new_sample.sr90_error, test_data['sr90_error'])
        self.assertEqual(new_sample.sr90_activity_per_calcium, test_data['sr90_activity_per_calcium'])
        
        # Check if the sample in the collection matches the input data
        stored_sample = self.service.samples[-1]
        self.assertEqual(stored_sample.sample_type, test_data['sample_type'])
        self.assertEqual(stored_sample.type, test_data['type'])
        self.assertEqual(stored_sample.start_date, test_data['start_date'])
        self.assertEqual(stored_sample.stop_date, test_data['stop_date'])
        self.assertEqual(stored_sample.station_name, test_data['station_name'])
        self.assertEqual(stored_sample.province, test_data['province'])
        self.assertEqual(stored_sample.sr90_activity, test_data['sr90_activity'])
        self.assertEqual(stored_sample.sr90_error, test_data['sr90_error'])
        self.assertEqual(stored_sample.sr90_activity_per_calcium, test_data['sr90_activity_per_calcium'])

if __name__ == '__main__':
    unittest.main() 