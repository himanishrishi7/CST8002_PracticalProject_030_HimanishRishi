"""
CST8002 - Practical Project 2
Professor: Tyler DeLay
Date: 15/05/2025
Author: Himanish Rishi

This module contains the MilkSampleService class which manages the business logic
for milk sample data. It is part of the Business Layer.

The service layer acts as an intermediary between the presentation layer and the
persistence layer, handling all business logic and data operations. It maintains
an in-memory collection of milk sample records and provides methods to manipulate
this data.

Key responsibilities:
- Managing the collection of milk samples in memory
- Providing business logic operations on the samples
- Coordinating with the persistence layer for file operations
- Validating data before storage
- Handling data transformations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import List, Optional, Tuple
from src.business.milk_sample_record import MilkSampleRecord
from src.persistence.milk_sample_repository import MilkSampleRepository

class MilkSampleService:
    """
    A service class that manages milk sample data and business logic.
    
    This class is responsible for:
    1. Managing the collection of milk samples
    2. Providing business logic operations on the samples
    3. Coordinating with the persistence layer
    4. Saving samples to new files
    5. Creating and storing new sample records
    6. Editing existing sample records
    7. Deleting sample records
    
    The service maintains an in-memory collection of MilkSampleRecord objects
    and provides methods to manipulate this data. It also coordinates with the
    persistence layer for file operations.
    
    Attributes:
        repository (MilkSampleRepository): The repository instance for file operations
        samples (List[MilkSampleRecord]): The in-memory collection of samples
    """
    
    def __init__(self):
        """
        Initialize the service with a repository and load up to 100 samples.
        
        The constructor creates a new repository instance and loads the initial
        set of samples from the data file. It sets up the basic structure needed
        for the service to operate.
        """
        self.repository = MilkSampleRepository()
        self.samples: List[MilkSampleRecord] = []
        self.load_samples(100)  # Load up to 100 samples on startup
    
    def load_samples(self, max_samples: int = 100) -> None:
        """
        Load samples from the repository.
        
        This method reads samples from the data file through the repository
        and stores them in the in-memory collection.
        
        Args:
            max_samples (int): Maximum number of samples to load (default: 100)
            
        Raises:
            FileNotFoundError: If the data file cannot be found
            ValueError: If there's an error parsing the data
        """
        self.samples = self.repository.read_samples(max_samples)
    
    def reload_samples(self, max_samples: int = 100) -> None:
        """
        Reload samples from the repository, replacing existing data.
        
        This method clears the current in-memory collection and loads a fresh
        set of samples from the data file.
        
        Args:
            max_samples (int): Maximum number of samples to load (default: 100)
            
        Raises:
            FileNotFoundError: If the data file cannot be found
            ValueError: If there's an error parsing the data
        """
        self.samples.clear()  # Clear existing samples
        self.load_samples(max_samples)  # Load new samples
    
    def get_sample(self, index: int) -> Optional[MilkSampleRecord]:
        """
        Get a sample by index.
        
        This method retrieves a specific sample from the in-memory collection
        based on its index.
        
        Args:
            index (int): Index of the sample to retrieve
            
        Returns:
            Optional[MilkSampleRecord]: The requested sample or None if not found
        """
        if 0 <= index < len(self.samples):
            return self.samples[index]
        return None
    
    def get_all_samples(self) -> List[MilkSampleRecord]:
        """
        Get all loaded samples.
        
        This method returns the complete in-memory collection of samples.
        
        Returns:
            List[MilkSampleRecord]: List of all samples
        """
        return self.samples
    
    def get_sample_count(self) -> int:
        """
        Get the number of loaded samples.
        
        This method returns the current size of the in-memory collection.
        
        Returns:
            int: Number of samples
        """
        return len(self.samples)
    
    def save_samples_to_new_file(self) -> str:
        """
        Save the current samples to a new CSV file with a unique identifier.
        
        This method coordinates with the repository to save the current
        in-memory collection to a new file with a unique name.
        
        Returns:
            str: The path to the newly created file
            
        Raises:
            IOError: If there's an error writing to the file
        """
        return self.repository.save_samples(self.samples)
    
    def create_new_sample(self, 
                         sample_type: str,
                         type: str,
                         start_date: str,
                         stop_date: str,
                         station_name: str,
                         province: str,
                         sr90_activity: float,
                         sr90_error: Optional[float] = None,
                         sr90_activity_per_calcium: Optional[float] = None) -> MilkSampleRecord:
        """
        Create a new milk sample record and add it to the in-memory collection.
        
        This method creates a new sample record with the provided data,
        validates the input, and adds it to the in-memory collection.
        
        Args:
            sample_type (str): Type of sample (e.g., MILK)
            type (str): Specific type of milk (e.g., WHOLE)
            start_date (str): Start date of the sampling period
            stop_date (str): End date of the sampling period
            station_name (str): Name of the sampling station
            province (str): Province where the sample was taken
            sr90_activity (float): Strontium-90 activity in Bq/L
            sr90_error (Optional[float]): Error in strontium-90 activity measurement
            sr90_activity_per_calcium (Optional[float]): Strontium-90 activity per calcium in Bq/g
            
        Returns:
            MilkSampleRecord: The newly created sample record
            
        Raises:
            ValueError: If required fields are invalid
        """
        # Validate required fields
        if not all([sample_type, type, start_date, stop_date, station_name, province]):
            raise ValueError("All fields except sr90_error and sr90_activity_per_calcium are required")
        
        if not isinstance(sr90_activity, (int, float)) or sr90_activity < 0:
            raise ValueError("Sr90 activity must be a non-negative number")
            
        # Create new record
        new_sample = MilkSampleRecord(
            sample_type=sample_type,
            type=type,
            start_date=start_date,
            stop_date=stop_date,
            station_name=station_name,
            province=province,
            sr90_activity=sr90_activity,
            sr90_error=sr90_error,
            sr90_activity_per_calcium=sr90_activity_per_calcium
        )
        
        # Add to in-memory collection
        self.samples.append(new_sample)
        return new_sample
    
    def edit_sample(self, index: int, **kwargs) -> Tuple[MilkSampleRecord, MilkSampleRecord]:
        """
        Edit an existing milk sample record.
        
        This method updates an existing sample record with new values,
        validates the changes, and updates the in-memory collection.
        
        Args:
            index (int): Index of the sample to edit
            **kwargs: Fields to update with their new values
            
        Returns:
            Tuple[MilkSampleRecord, MilkSampleRecord]: Tuple containing (old_record, new_record)
            
        Raises:
            IndexError: If the index is out of range
            ValueError: If any of the updated fields are invalid
        """
        if not 0 <= index < len(self.samples):
            raise IndexError(f"Index {index} is out of range")
            
        old_record = self.samples[index]
        
        # Create a new record with updated values
        new_values = {
            'sample_type': kwargs.get('sample_type', old_record.sample_type),
            'type': kwargs.get('type', old_record.type),
            'start_date': kwargs.get('start_date', old_record.start_date),
            'stop_date': kwargs.get('stop_date', old_record.stop_date),
            'station_name': kwargs.get('station_name', old_record.station_name),
            'province': kwargs.get('province', old_record.province),
            'sr90_activity': kwargs.get('sr90_activity', old_record.sr90_activity),
            'sr90_error': kwargs.get('sr90_error', old_record.sr90_error),
            'sr90_activity_per_calcium': kwargs.get('sr90_activity_per_calcium', old_record.sr90_activity_per_calcium)
        }
        
        # Validate required fields
        if not all([new_values['sample_type'], new_values['type'], 
                   new_values['start_date'], new_values['stop_date'],
                   new_values['station_name'], new_values['province']]):
            raise ValueError("All fields except sr90_error and sr90_activity_per_calcium are required")
        
        # Validate numeric fields
        if not isinstance(new_values['sr90_activity'], (int, float)) or new_values['sr90_activity'] < 0:
            raise ValueError("Sr90 activity must be a non-negative number")
            
        # Create new record
        new_record = MilkSampleRecord(**new_values)
        
        # Update the record in the collection
        self.samples[index] = new_record
        
        return old_record, new_record
    
    def delete_sample(self, index: int) -> MilkSampleRecord:
        """
        Delete a milk sample record from the in-memory collection.
        
        This method removes a sample record from the in-memory collection
        based on its index.
        
        Args:
            index (int): Index of the sample to delete
            
        Returns:
            MilkSampleRecord: The deleted sample record
            
        Raises:
            IndexError: If the index is out of range
        """
        if not 0 <= index < len(self.samples):
            raise IndexError(f"Index {index} is out of range")
            
        # Remove and return the deleted record
        return self.samples.pop(index) 