"""
CST8002 - Practical Project 2
Professor: Tyler DeLay
Date: 15/05/2025
Author: Himanish Rishi

This module contains the MilkSampleRecord class which represents a single record
from the strontium-90 milk sample dataset. It is part of the Model Layer.

The model layer is responsible for:
- Defining the data structures used in the application
- Providing data validation and type conversion
- Maintaining data integrity
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class MilkSampleRecord:
    """
    A record object representing a milk sample measurement from the dataset.
    This class uses the exact column names from the CSV file as field names.
    
    The class is implemented as a dataclass to automatically generate:
    - __init__ method
    - __repr__ method
    - __eq__ method
    - Other special methods
    
    Attributes:
        sample_type (str): Type of sample (e.g., MILK)
        type (str): Specific type of milk (e.g., WHOLE)
        start_date (str): Start date of the sampling period
        stop_date (str): End date of the sampling period
        station_name (str): Name of the sampling station
        province (str): Province where the sample was taken
        sr90_activity (float): Strontium-90 activity in Bq/L
        sr90_error (Optional[float]): Error in strontium-90 activity measurement
        sr90_activity_per_calcium (Optional[float]): Strontium-90 activity per calcium in Bq/g
    """
    # Column names from CSV file
    sample_type: str  # "Sample Type/ Type d'échantillon"
    type: str  # "Type"
    start_date: str  # "Start Date/ Date de Début"
    stop_date: str  # "Stop Date/ Date de Fin"
    station_name: str  # "Station Name/ Nom de Station"
    province: str  # "Province"
    sr90_activity: float  # "Sr90 Activity/ Activité (Bq/L)"
    sr90_error: Optional[float]  # "Sr90 Error/ Erreur (Bq/L)"
    sr90_activity_per_calcium: Optional[float]  # "Sr90 Activity/Calcium (Bq/g)"
    
    def __post_init__(self):
        """
        Convert string values to appropriate types after initialization.
        This method is automatically called after __init__ when using @dataclass.
        
        The method:
        1. Converts empty strings to None for optional fields
        2. Converts string values to float for numeric fields
        3. Ensures data type consistency
        """
        # Convert empty strings to None for optional fields
        if self.sr90_error == "":
            self.sr90_error = None
        if self.sr90_activity_per_calcium == "":
            self.sr90_activity_per_calcium = None
            
        # Convert string values to float for numeric fields
        if isinstance(self.sr90_activity, str):
            self.sr90_activity = float(self.sr90_activity) if self.sr90_activity else 0.0
        if isinstance(self.sr90_error, str):
            self.sr90_error = float(self.sr90_error) if self.sr90_error else None
        if isinstance(self.sr90_activity_per_calcium, str):
            self.sr90_activity_per_calcium = float(self.sr90_activity_per_calcium) if self.sr90_activity_per_calcium else None 