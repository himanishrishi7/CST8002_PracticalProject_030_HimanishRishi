"""
CST8002 - Practical Project 2
Professor: Tyler DeLay
Date: 15/05/2025
Author: Himanish Rishi

This module contains the MilkSampleDBRepository class which handles all database operations
for the milk sample data. It is part of the Persistence Layer.

This module replaces the file-based repository with database operations including:
- CREATE: Insert new milk sample records
- READ: Retrieve milk sample records with various filters
- UPDATE: Modify existing milk sample records
- DELETE: Remove milk sample records
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import sqlite3
from typing import List, Optional, Dict, Any
from src.model.milk_sample_record import MilkSampleRecord
from src.persistence.database_config import DatabaseConfig

class MilkSampleDBRepository:
    """
    A class to handle database operations for milk sample data.
    
    This class is responsible for:
    1. Creating new milk sample records in the database
    2. Reading milk sample records from the database
    3. Updating existing milk sample records
    4. Deleting milk sample records
    5. Converting between database rows and MilkSampleRecord objects
    6. Error handling for database operations
    """
    
    def __init__(self, db_config: Optional[DatabaseConfig] = None):
        """
        Initialize the repository with database configuration.
        
        Args:
            db_config (Optional[DatabaseConfig]): Database configuration instance
        """
        self.db_config = db_config or DatabaseConfig()
        self.initialize_database()
    
    def initialize_database(self) -> None:
        """Initialize the database table."""
        self.db_config.initialize_database()
    
    def _row_to_record(self, row: sqlite3.Row) -> MilkSampleRecord:
        """
        Convert a database row to a MilkSampleRecord object.
        
        Args:
            row (sqlite3.Row): Database row
            
        Returns:
            MilkSampleRecord: Converted record object
        """
        return MilkSampleRecord(
            sample_type=row['sample_type'],
            type=row['type'],
            start_date=row['start_date'],
            stop_date=row['stop_date'],
            station_name=row['station_name'],
            province=row['province'],
            sr90_activity=float(row['sr90_activity']),
            sr90_error=float(row['sr90_error']) if row['sr90_error'] is not None else None,
            sr90_activity_per_calcium=float(row['sr90_activity_per_calcium']) if row['sr90_activity_per_calcium'] is not None else None
        )
    
    def _record_to_dict(self, record: MilkSampleRecord) -> Dict[str, Any]:
        """
        Convert a MilkSampleRecord object to a dictionary for database operations.
        
        Args:
            record (MilkSampleRecord): Record object
            
        Returns:
            Dict[str, Any]: Dictionary representation
        """
        return {
            'sample_type': record.sample_type,
            'type': record.type,
            'start_date': record.start_date,
            'stop_date': record.stop_date,
            'station_name': record.station_name,
            'province': record.province,
            'sr90_activity': record.sr90_activity,
            'sr90_error': record.sr90_error,
            'sr90_activity_per_calcium': record.sr90_activity_per_calcium
        }
    
    def create_sample(self, record: MilkSampleRecord) -> int:
        """
        Create a new milk sample record in the database.
        
        Args:
            record (MilkSampleRecord): Record to create
            
        Returns:
            int: ID of the newly created record
            
        Raises:
            sqlite3.Error: If there's an error inserting the record
        """
        insert_sql = """
        INSERT INTO milk_samples (
            sample_type, type, start_date, stop_date, station_name, 
            province, sr90_activity, sr90_error, sr90_activity_per_calcium
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            with self.db_config.get_db_context() as conn:
                cursor = conn.cursor()
                data = self._record_to_dict(record)
                cursor.execute(insert_sql, (
                    data['sample_type'], data['type'], data['start_date'],
                    data['stop_date'], data['station_name'], data['province'],
                    data['sr90_activity'], data['sr90_error'], data['sr90_activity_per_calcium']
                ))
                conn.commit()
                record_id = cursor.lastrowid
                print(f"Created new milk sample record with ID: {record_id}")
                return record_id
        except sqlite3.Error as e:
            print(f"Error creating milk sample record: {e}")
            raise
    
    def read_sample_by_id(self, record_id: int) -> Optional[MilkSampleRecord]:
        """
        Read a milk sample record by its ID.
        
        Args:
            record_id (int): ID of the record to retrieve
            
        Returns:
            Optional[MilkSampleRecord]: The requested record or None if not found
            
        Raises:
            sqlite3.Error: If there's an error reading the record
        """
        select_sql = "SELECT * FROM milk_samples WHERE id = ?"
        
        try:
            with self.db_config.get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute(select_sql, (record_id,))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_record(row)
                return None
        except sqlite3.Error as e:
            print(f"Error reading milk sample record: {e}")
            raise
    
    def read_all_samples(self, limit: Optional[int] = None, offset: int = 0) -> List[MilkSampleRecord]:
        """
        Read all milk sample records from the database.
        
        Args:
            limit (Optional[int]): Maximum number of records to retrieve
            offset (int): Number of records to skip
            
        Returns:
            List[MilkSampleRecord]: List of milk sample records
            
        Raises:
            sqlite3.Error: If there's an error reading the records
        """
        if limit:
            select_sql = "SELECT * FROM milk_samples ORDER BY id LIMIT ? OFFSET ?"
            params = (limit, offset)
        else:
            select_sql = "SELECT * FROM milk_samples ORDER BY id"
            params = ()
        
        try:
            with self.db_config.get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute(select_sql, params)
                rows = cursor.fetchall()
                
                records = []
                for row in rows:
                    records.append(self._row_to_record(row))
                
                print(f"Retrieved {len(records)} milk sample records")
                return records
        except sqlite3.Error as e:
            print(f"Error reading milk sample records: {e}")
            raise
    
    def read_samples_by_province(self, province: str) -> List[MilkSampleRecord]:
        """
        Read milk sample records filtered by province.
        
        Args:
            province (str): Province to filter by
            
        Returns:
            List[MilkSampleRecord]: List of milk sample records for the province
            
        Raises:
            sqlite3.Error: If there's an error reading the records
        """
        select_sql = "SELECT * FROM milk_samples WHERE province = ? ORDER BY id"
        
        try:
            with self.db_config.get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute(select_sql, (province,))
                rows = cursor.fetchall()
                
                records = []
                for row in rows:
                    records.append(self._row_to_record(row))
                
                print(f"Retrieved {len(records)} milk sample records for province: {province}")
                return records
        except sqlite3.Error as e:
            print(f"Error reading milk sample records by province: {e}")
            raise
    
    def read_samples_by_station(self, station_name: str) -> List[MilkSampleRecord]:
        """
        Read milk sample records filtered by station name.
        
        Args:
            station_name (str): Station name to filter by
            
        Returns:
            List[MilkSampleRecord]: List of milk sample records for the station
            
        Raises:
            sqlite3.Error: If there's an error reading the records
        """
        select_sql = "SELECT * FROM milk_samples WHERE station_name = ? ORDER BY id"
        
        try:
            with self.db_config.get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute(select_sql, (station_name,))
                rows = cursor.fetchall()
                
                records = []
                for row in rows:
                    records.append(self._row_to_record(row))
                
                print(f"Retrieved {len(records)} milk sample records for station: {station_name}")
                return records
        except sqlite3.Error as e:
            print(f"Error reading milk sample records by station: {e}")
            raise
    
    def update_sample(self, record_id: int, record: MilkSampleRecord) -> bool:
        """
        Update an existing milk sample record in the database.
        
        Args:
            record_id (int): ID of the record to update
            record (MilkSampleRecord): Updated record data
            
        Returns:
            bool: True if record was updated, False if not found
            
        Raises:
            sqlite3.Error: If there's an error updating the record
        """
        update_sql = """
        UPDATE milk_samples SET 
            sample_type = ?, type = ?, start_date = ?, stop_date = ?,
            station_name = ?, province = ?, sr90_activity = ?, 
            sr90_error = ?, sr90_activity_per_calcium = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """
        
        try:
            with self.db_config.get_db_context() as conn:
                cursor = conn.cursor()
                data = self._record_to_dict(record)
                cursor.execute(update_sql, (
                    data['sample_type'], data['type'], data['start_date'],
                    data['stop_date'], data['station_name'], data['province'],
                    data['sr90_activity'], data['sr90_error'], data['sr90_activity_per_calcium'],
                    record_id
                ))
                conn.commit()
                
                if cursor.rowcount > 0:
                    print(f"Updated milk sample record with ID: {record_id}")
                    return True
                else:
                    print(f"No milk sample record found with ID: {record_id}")
                    return False
        except sqlite3.Error as e:
            print(f"Error updating milk sample record: {e}")
            raise
    
    def delete_sample(self, record_id: int) -> bool:
        """
        Delete a milk sample record from the database.
        
        Args:
            record_id (int): ID of the record to delete
            
        Returns:
            bool: True if record was deleted, False if not found
            
        Raises:
            sqlite3.Error: If there's an error deleting the record
        """
        delete_sql = "DELETE FROM milk_samples WHERE id = ?"
        
        try:
            with self.db_config.get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute(delete_sql, (record_id,))
                conn.commit()
                
                if cursor.rowcount > 0:
                    print(f"Deleted milk sample record with ID: {record_id}")
                    return True
                else:
                    print(f"No milk sample record found with ID: {record_id}")
                    return False
        except sqlite3.Error as e:
            print(f"Error deleting milk sample record: {e}")
            raise
    
    def get_sample_count(self) -> int:
        """
        Get the total number of milk sample records in the database.
        
        Returns:
            int: Total number of records
            
        Raises:
            sqlite3.Error: If there's an error counting the records
        """
        count_sql = "SELECT COUNT(*) FROM milk_samples"
        
        try:
            with self.db_config.get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute(count_sql)
                count = cursor.fetchone()[0]
                return count
        except sqlite3.Error as e:
            print(f"Error counting milk sample records: {e}")
            raise
    
    def clear_all_samples(self) -> int:
        """
        Delete all milk sample records from the database.
        
        Returns:
            int: Number of records deleted
            
        Raises:
            sqlite3.Error: If there's an error deleting the records
        """
        delete_sql = "DELETE FROM milk_samples"
        
        try:
            with self.db_config.get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute(delete_sql)
                conn.commit()
                deleted_count = cursor.rowcount
                print(f"Deleted {deleted_count} milk sample records")
                return deleted_count
        except sqlite3.Error as e:
            print(f"Error clearing milk sample records: {e}")
            raise 