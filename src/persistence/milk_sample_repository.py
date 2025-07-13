"""
CST8002 - Practical Project 3
Professor: Tyler DeLay
Due Date: 25/05/2025
Author: Himanish Rishi

This module contains the MilkSampleRepository class which handles all file I/O operations
for the milk sample data. It is part of the Persistence Layer.
"""

import sys
import os
import uuid
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import csv
from typing import List, Optional
from src.business.milk_sample_record import MilkSampleRecord

class MilkSampleRepository:
    """
    A class to handle file I/O operations for milk sample data.
    
    This class is responsible for:
    1. Reading data from the CSV file
    2. Converting raw data into MilkSampleRecord objects
    3. Error handling for file operations
    4. Saving data to new CSV files with unique identifiers
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
        skipped_rows = 0
        total_rows = 0
        try:
            with open(self.filename, "r", encoding="utf-8-sig", errors='ignore') as f:
                csv_reader = csv.reader(f)
                next(csv_reader)  # Skip header
                
                for row_num, values in enumerate(csv_reader, start=2):  # start=2 because we skipped header
                    total_rows += 1
                    if len(samples) >= max_samples:
                        break
                        
                    try:
                        # Clean and validate values
                        cleaned_values = [v.strip() for v in values if v.strip()]
                        
                        if len(cleaned_values) < 9:
                            print(f"Skipping row {row_num}: Insufficient values (found {len(cleaned_values)}, need 9)")
                            print(f"Row data: {values}")
                            skipped_rows += 1
                            continue
                            
                        sample = MilkSampleRecord(
                            sample_type=cleaned_values[0],
                            type=cleaned_values[1],
                            start_date=cleaned_values[2],
                            stop_date=cleaned_values[3],
                            station_name=cleaned_values[4],
                            province=cleaned_values[5],
                            sr90_activity=cleaned_values[6],
                            sr90_error=cleaned_values[7],
                            sr90_activity_per_calcium=cleaned_values[8]
                        )
                        samples.append(sample)
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing row {row_num}: {str(e)}")
                        print(f"Row data: {values}")
                        skipped_rows += 1
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
            
        print(f"\nFile Statistics:")
        print(f"Total rows processed: {total_rows}")
        print(f"Rows skipped: {skipped_rows}")
        print(f"Rows successfully loaded: {len(samples)}")
        print(f"Maximum samples requested: {max_samples}")
        
        return samples

    def save_samples(self, samples: List[MilkSampleRecord]) -> str:
        """
        Save samples to a new CSV file with a UUID-based filename.
        
        Args:
            samples (List[MilkSampleRecord]): List of samples to save
            
        Returns:
            str: The path to the newly created file
            
        Raises:
            IOError: If there's an error writing to the file
        """
        # Generate a unique filename using UUID
        unique_filename = f"milk_samples_{uuid.uuid4()}.csv"
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output_path = os.path.join(current_dir, unique_filename)
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    "Sample Type/ Type d'échantillon",
                    "Type",
                    "Start Date/ Date de Début",
                    "Stop Date/ Date de Fin",
                    "Station Name/ Nom de Station",
                    "Province",
                    "Sr90 Activity/ Activité (Bq/L)",
                    "Sr90 Error/ Erreur (Bq/L)",
                    "Sr90 Activity/Calcium (Bq/g)"
                ])
                
                # Write data rows
                for sample in samples:
                    writer.writerow([
                        sample.sample_type,
                        sample.type,
                        sample.start_date,
                        sample.stop_date,
                        sample.station_name,
                        sample.province,
                        sample.sr90_activity,
                        sample.sr90_error if sample.sr90_error is not None else "",
                        sample.sr90_activity_per_calcium if sample.sr90_activity_per_calcium is not None else ""
                    ])
                    
            print(f"Successfully saved {len(samples)} samples to {output_path}")
            return output_path
            
        except IOError as e:
            print(f"Error saving samples to file: {str(e)}")
            raise 