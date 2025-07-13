"""
CST8002 - Practical Project 3
Professor: Tyler DeLay
Date: 13/07/2025
Author: Himanish Rishi

This module contains the MilkSampleDBService class which manages the business logic
for milk sample data using database operations. It is part of the Business Layer.

This module replaces the file-based service with database operations including:
- CREATE: Create new milk sample records
- READ: Retrieve milk sample records with various filters
- UPDATE: Modify existing milk sample records
- DELETE: Remove milk sample records
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import List, Optional, Tuple
from src.model.milk_sample_record import MilkSampleRecord
from src.persistence.milk_sample_db_repository import MilkSampleDBRepository

class MilkSampleDBService:
    """
    A service class that manages milk sample data and business logic using database operations.
    
    This class is responsible for:
    1. Managing milk sample data through database operations
    2. Providing business logic operations on the samples
    3. Coordinating with the database repository
    4. Creating and storing new sample records
    5. Editing existing sample records
    6. Deleting sample records
    7. Providing filtered data access
    
    The service uses the database repository for all data operations and provides
    a clean interface for the presentation layer to interact with the data.
    
    Attributes:
        repository (MilkSampleDBRepository): The database repository instance
    """
    
    def __init__(self, repository: Optional[MilkSampleDBRepository] = None):
        """
        Initialize the service with a database repository.
        
        The constructor creates a new database repository instance and sets up
        the basic structure needed for the service to operate.
        
        Args:
            repository (Optional[MilkSampleDBRepository]): Database repository instance
        """
        self.repository = repository or MilkSampleDBRepository()
    
    def get_sample_by_id(self, record_id: int) -> Optional[MilkSampleRecord]:
        """
        Get a sample by its database ID.
        
        This method retrieves a specific sample from the database
        based on its unique ID.
        
        Args:
            record_id (int): Database ID of the sample to retrieve
            
        Returns:
            Optional[MilkSampleRecord]: The requested sample or None if not found
        """
        return self.repository.read_sample_by_id(record_id)
    
    def get_all_samples(self, limit: Optional[int] = None, offset: int = 0) -> List[MilkSampleRecord]:
        """
        Get all samples from the database.
        
        This method returns samples from the database with optional
        pagination support.
        
        Args:
            limit (Optional[int]): Maximum number of samples to retrieve
            offset (int): Number of samples to skip
            
        Returns:
            List[MilkSampleRecord]: List of all samples
        """
        return self.repository.read_all_samples_simple(limit, offset)
    
    def get_all_samples_with_ids(self, limit: Optional[int] = None, offset: int = 0) -> List[Tuple[int, MilkSampleRecord]]:
        """
        Get all samples from the database with their actual IDs.
        
        Args:
            limit (Optional[int]): Maximum number of records to retrieve
            offset (int): Number of records to skip
            
        Returns:
            List[Tuple[int, MilkSampleRecord]]: List of tuples containing (id, record)
        """
        return self.repository.read_all_samples(limit, offset)
    
    def get_samples_by_province(self, province: str) -> List[MilkSampleRecord]:
        """
        Get samples filtered by province.
        
        This method returns all samples from a specific province.
        
        Args:
            province (str): Province to filter by
            
        Returns:
            List[MilkSampleRecord]: List of samples for the province
        """
        return self.repository.read_samples_by_province(province)
    
    def get_samples_by_station(self, station_name: str) -> List[MilkSampleRecord]:
        """
        Get samples filtered by station name.
        
        This method returns all samples from a specific station.
        
        Args:
            station_name (str): Station name to filter by
            
        Returns:
            List[MilkSampleRecord]: List of samples for the station
        """
        return self.repository.read_samples_by_station(station_name)
    
    def get_sample_count(self) -> int:
        """
        Get the total number of samples in the database.
        
        This method returns the current count of all samples in the database.
        
        Returns:
            int: Total number of samples
        """
        return self.repository.get_sample_count()
    
    def create_new_sample(self, 
                         sample_type: str,
                         type: str,
                         start_date: str,
                         stop_date: str,
                         station_name: str,
                         province: str,
                         sr90_activity: float,
                         sr90_error: Optional[float] = None,
                         sr90_activity_per_calcium: Optional[float] = None) -> Tuple[int, MilkSampleRecord]:
        """
        Create a new milk sample record and store it in the database.
        
        This method creates a new sample record with the provided data,
        validates the input, and stores it in the database.
        
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
            Tuple[int, MilkSampleRecord]: Tuple containing (record_id, new_record)
            
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
        
        # Store in database
        record_id = self.repository.create_sample(new_sample)
        return record_id, new_sample
    
    def edit_sample(self, record_id: int, **kwargs) -> Tuple[bool, Optional[MilkSampleRecord], Optional[MilkSampleRecord]]:
        """
        Edit an existing milk sample record in the database.
        
        This method updates an existing sample record with new values,
        validates the changes, and updates the database.
        
        Args:
            record_id (int): Database ID of the sample to edit
            **kwargs: Fields to update with their new values
            
        Returns:
            Tuple[bool, Optional[MilkSampleRecord], Optional[MilkSampleRecord]]: 
            Tuple containing (success, old_record, new_record)
            
        Raises:
            ValueError: If any of the updated fields are invalid
        """
        # Get existing record
        old_record = self.repository.read_sample_by_id(record_id)
        if not old_record:
            return False, None, None
        
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
        
        if not isinstance(new_values['sr90_activity'], (int, float)) or new_values['sr90_activity'] < 0:
            raise ValueError("Sr90 activity must be a non-negative number")
        
        # Create updated record
        updated_record = MilkSampleRecord(
            sample_type=new_values['sample_type'],
            type=new_values['type'],
            start_date=new_values['start_date'],
            stop_date=new_values['stop_date'],
            station_name=new_values['station_name'],
            province=new_values['province'],
            sr90_activity=new_values['sr90_activity'],
            sr90_error=new_values['sr90_error'],
            sr90_activity_per_calcium=new_values['sr90_activity_per_calcium']
        )
        
        # Update in database
        success = self.repository.update_sample(record_id, updated_record)
        return success, old_record, updated_record
    
    def delete_sample(self, record_id: int) -> Tuple[bool, Optional[MilkSampleRecord]]:
        """
        Delete a milk sample record from the database.
        
        This method removes a specific sample record from the database
        based on its unique ID.
        
        Args:
            record_id (int): Database ID of the sample to delete
            
        Returns:
            Tuple[bool, Optional[MilkSampleRecord]]: Tuple containing (success, deleted_record)
        """
        # Get the record before deleting
        record_to_delete = self.repository.read_sample_by_id(record_id)
        if not record_to_delete:
            return False, None
        
        # Delete from database
        success = self.repository.delete_sample(record_id)
        return success, record_to_delete
    
    def get_available_provinces(self) -> List[str]:
        """
        Get a list of all available provinces in the database.
        
        Returns:
            List[str]: List of unique province names
        """
        all_samples = self.repository.read_all_samples()
        provinces = set()
        for _, sample in all_samples:  # Unpack the tuple (id, record)
            provinces.add(sample.province)
        return sorted(list(provinces))
    
    def get_available_stations(self) -> List[str]:
        """
        Get a list of all available stations in the database.
        
        Returns:
            List[str]: List of unique station names
        """
        all_samples = self.repository.read_all_samples()
        stations = set()
        for _, sample in all_samples:  # Unpack the tuple (id, record)
            stations.add(sample.station_name)
        return sorted(list(stations))
    
    def get_statistics(self) -> dict:
        """
        Get comprehensive statistics about the milk sample data.
        
        Returns:
            dict: Dictionary containing various statistics
        """
        total_count = self.repository.get_sample_count()
        all_samples = self.repository.read_all_samples()
        
        # Calculate statistics
        provinces = set()
        stations = set()
        total_activity = 0.0
        valid_activity_count = 0
        
        for _, sample in all_samples:  # Unpack the tuple (id, record)
            provinces.add(sample.province)
            stations.add(sample.station_name)
            if sample.sr90_activity is not None and sample.sr90_activity > 0:
                total_activity += sample.sr90_activity
                valid_activity_count += 1
        
        avg_activity = total_activity / valid_activity_count if valid_activity_count > 0 else 0
        
        stats = {
            'total_samples': total_count,
            'unique_provinces': len(provinces),
            'unique_stations': len(stations),
            'provinces': sorted(list(provinces)),
            'stations': sorted(list(stations)),
            'average_sr90_activity': avg_activity,
            'valid_activity_readings': valid_activity_count
        }
        
        return stats 