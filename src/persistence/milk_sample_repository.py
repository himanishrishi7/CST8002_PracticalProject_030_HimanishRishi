"""
CST8002 - Practical Project 2
Professor: Tyler DeLay
Due Date: 25/05/2025
Author: Himanish Rishi

This module contains the MilkSampleRepository class which handles all file I/O operations
for the milk sample data. It is part of the Persistence Layer.
"""

import csv
import os
from typing import List, Optional
from src.business.milk_sample_record import MilkSampleRecord

class MilkSampleRepository:
    """
    A class to handle file I/O operations for milk sample data.
    
    This class is responsible for:
    1. Reading data from the CSV file
    2. Converting raw data into MilkSampleRecord objects
    3. Error handling for file operations
    """
    
    def __init__(self):
        """Initialize the repository with the CSV file path."""
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.filename = os.path.join(current_dir, "nms_strontium90_milk_ssn_strontium90_lait.csv")
        
        if not os.path.exists(self.filename):
            print(f"Warning: File not found at {self.filename}")
            print("Current directory contents:")
            for file in os.listdir(current_dir):
                print(f"  - {file}")
    
    def read_samples(self, max_samples: int = 100) -> List[MilkSampleRecord]:
        """
        Read up to the specified number of samples from the CSV file.
        
        Args:
            max_samples (int): Maximum number of samples to read (default: 100)
            
        Returns:
            List[MilkSampleRecord]: List of parsed sample records
            
        Raises:
            FileNotFoundError: If the CSV file is not found
            ValueError: If there's an error parsing the data
        """
        samples = []
        try:
            with open(self.filename, "r", encoding="utf-8-sig", errors='ignore') as f:
                csv_reader = csv.reader(f)
                next(csv_reader)  # Skip header
                
                for _ in range(max_samples):
                    try:
                        values = next(csv_reader)
                        values = [v.strip() for v in values if v.strip()]
                        
                        if len(values) >= 9:
                            sample = MilkSampleRecord(
                                sample_type=values[0],
                                type=values[1],
                                start_date=values[2],
                                stop_date=values[3],
                                station_name=values[4],
                                province=values[5],
                                sr90_activity=values[6],
                                sr90_error=values[7],
                                sr90_activity_per_calcium=values[8]
                            )
                            samples.append(sample)
                    except StopIteration:
                        # End of file reached
                        break
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing line: {values}")
                        print(f"Error details: {str(e)}")
                        continue
                        
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            print(f"Current working directory: {os.getcwd()}")
            print("Directory contents:")
            for file in os.listdir(os.getcwd()):
                print(f"  - {file}")
            raise
        except Exception as e:
            print(f"Unexpected error reading file: {str(e)}")
            raise
            
        print(f"Successfully loaded {len(samples)} samples from the CSV file.")
        return samples 