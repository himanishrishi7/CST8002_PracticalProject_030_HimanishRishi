"""
CST8002 - Practical Project 3
Professor: Tyler DeLay
Date: 13/07/2025
Author: Himanish Rishi

This module contains the database configuration and connection setup.
It is part of the Persistence Layer.

This module is responsible for:
- Database connection setup
- Database initialization
- Connection management
"""

import sqlite3
import os
from typing import Optional
from contextlib import contextmanager

class DatabaseConfig:
    """
    A class to handle database configuration and connection management.
    
    This class is responsible for:
    1. Setting up the database connection
    2. Creating the database file if it doesn't exist
    3. Managing database connections
    4. Providing connection context management
    """
    
    def __init__(self, db_name: str = "milk_samples.db"):
        """
        Initialize the database configuration.
        
        Args:
            db_name (str): Name of the database file (default: milk_samples.db)
        """
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.db_path = os.path.join(current_dir, db_name)
        self.connection: Optional[sqlite3.Connection] = None
        
    def get_connection(self) -> sqlite3.Connection:
        """
        Get a database connection, creating it if necessary.
        
        Returns:
            sqlite3.Connection: Database connection
            
        Raises:
            sqlite3.Error: If there's an error connecting to the database
        """
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(self.db_path)
                self.connection.row_factory = sqlite3.Row  # Enable row factory for named access
                print(f"Connected to database: {self.db_path}")
            except sqlite3.Error as e:
                print(f"Error connecting to database: {e}")
                raise
        return self.connection
    
    def close_connection(self) -> None:
        """Close the database connection if it exists."""
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Database connection closed")
    
    @contextmanager
    def get_db_context(self):
        """
        Context manager for database operations.
        
        This method provides a context manager that automatically
        handles connection creation and cleanup.
        
        Yields:
            sqlite3.Connection: Database connection
        """
        connection = self.get_connection()
        try:
            yield connection
        except Exception as e:
            connection.rollback()
            raise
        finally:
            # Don't close the connection here as it might be reused
            pass
    
    def initialize_database(self) -> None:
        """
        Initialize the database by creating the milk_samples table.
        
        This method creates the database table with the appropriate schema
        based on the CSV column structure.
        
        Raises:
            sqlite3.Error: If there's an error creating the table
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS milk_samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_type TEXT NOT NULL,
            type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            stop_date TEXT NOT NULL,
            station_name TEXT NOT NULL,
            province TEXT NOT NULL,
            sr90_activity REAL NOT NULL,
            sr90_error REAL,
            sr90_activity_per_calcium REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        try:
            with self.get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute(create_table_sql)
                conn.commit()
                print("Database table 'milk_samples' created successfully")
        except sqlite3.Error as e:
            print(f"Error creating database table: {e}")
            raise
    
    def drop_table(self) -> None:
        """
        Drop the milk_samples table (for testing/reset purposes).
        
        Raises:
            sqlite3.Error: If there's an error dropping the table
        """
        drop_table_sql = "DROP TABLE IF EXISTS milk_samples"
        
        try:
            with self.get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute(drop_table_sql)
                conn.commit()
                print("Database table 'milk_samples' dropped successfully")
        except sqlite3.Error as e:
            print(f"Error dropping database table: {e}")
            raise 