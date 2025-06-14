"""
CST8002 - Practical Project 1
Professor: Tyler DeLay
Due Date: 25/05/2025
Author: Himanish Rishi

This module contains classes for reading and managing milk sample data from a CSV file.
It includes the SampleCollection class for storing individual sample records and the
MilkSampleReader class for reading and parsing the CSV data.
"""

import csv
import os
from typing import Optional
from milk_sample_record import MilkSampleRecord


# Author information
AUTHOR_NAME = "Himanish Rishi"
class SampleCollection:
    """
    A class to hold individual sample objects.
    
    This class stores up to five MilkSampleRecord objects as individual attributes,
    providing a structured way to access specific samples without using a list.
    
    Attributes:
        sample1 (Optional[MilkSampleRecord]): First sample record
        sample2 (Optional[MilkSampleRecord]): Second sample record
        sample3 (Optional[MilkSampleRecord]): Third sample record
        sample4 (Optional[MilkSampleRecord]): Fourth sample record
        sample5 (Optional[MilkSampleRecord]): Fifth sample record
    """
    def __init__(self):
        """
        Initialize a new SampleCollection with all sample attributes set to None.
        """
        self.sample1: Optional[MilkSampleRecord] = None
        self.sample2: Optional[MilkSampleRecord] = None
        self.sample3: Optional[MilkSampleRecord] = None
        self.sample4: Optional[MilkSampleRecord] = None
        self.sample5: Optional[MilkSampleRecord] = None
        self.sample6: Optional[MilkSampleRecord] = None

class MilkSampleReader:
    """
    A class to read milk sample data from a CSV file and store it in individual record objects.
    
    This class handles file I/O operations, data parsing, and error handling for the
    milk sample dataset. It uses SampleCollection to store the parsed records.
    
    Attributes:
        filename (str): Path to the CSV file
        samples (SampleCollection): Collection of parsed sample records
    """
    def __init__(self):
        """
        Initialize the MilkSampleReader with the CSV file path.
        
        The method:
        1. Constructs the absolute path to the CSV file
        2. Creates a new SampleCollection
        3. Verifies the file exists
        """
        # Get the absolute path of the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the absolute path to the CSV file
        self.filename = os.path.join(current_dir, "nms_strontium90_milk_ssn_strontium90_lait.csv")
        self.samples = SampleCollection()
        
        # Verify file exists during initialization
        if not os.path.exists(self.filename):
            print(f"Warning: File not found at {self.filename}")
            print("Current directory contents:")
            for file in os.listdir(current_dir):
                print(f"  - {file}")

    def read_samples(self, num_samples: int = 6) -> SampleCollection:
        """
        Read the specified number of samples from the CSV file and store them as individual record objects.
        
        Args:
            num_samples (int): Number of samples to read (default: 5)
            
        Returns:
            SampleCollection: Collection of MilkSampleRecord objects
            
        Raises:
            FileNotFoundError: If the CSV file is not found
            ValueError: If there's an error parsing the data
            Exception: For any other unexpected errors
        """
        try:
            print(f"Attempting to open file: {self.filename}")
            with open(self.filename, "r", encoding="utf-8-sig", errors='ignore') as f:
                csv_reader = csv.reader(f)
                # Skip header row
                next(csv_reader)
                
                # Read specified number of records
                for i in range(num_samples):
                    try:
                        values = next(csv_reader)
                        # Remove any empty fields
                        values = [v.strip() for v in values if v.strip()]
                        
                        if len(values) >= 9:
                            # Create a new MilkSampleRecord object
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
                            # Store in the appropriate sample attribute
                            setattr(self.samples, f'sample{i+1}', sample)
                    except StopIteration:
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
            
        return self.samples

    def display_samples(self):
        """
        Display all samples in the data structure in a formatted way.
        
        This method:
        1. Prints a header for the data display
        2. Iterates through all samples in the collection
        3. Formats and displays each sample's data
        4. Handles optional fields appropriately
        """
        print("\n" + "="*80)
        print("MILK SAMPLE DATA".center(80))
        print("="*80)

        for i in range(1, 9):
            sample = getattr(self.samples, f'sample{i}')
            if sample is None:
                continue
                
            print(f"\nSample #{i}")
            print("-"*40)
            print(f"Sample Type: {sample.sample_type}")
            print(f"Type: {sample.type}")
            print(f"Date Range: {sample.start_date} to {sample.stop_date}")
            print(f"Location: {sample.station_name}, {sample.province}")
            print(f"Sr-90 Activity: {sample.sr90_activity:.2e} Bq/L")
            if sample.sr90_error is not None:
                print(f"Sr-90 Error: {sample.sr90_error:.2e} Bq/L")
            if sample.sr90_activity_per_calcium is not None:
                print(f"Sr-90 Activity/Calcium: {sample.sr90_activity_per_calcium:.2e} Bq/g")
            print("-"*40)

def main():
    """
    Main function to demonstrate the MilkSampleReader functionality.
    
    This function:
    1. Creates a MilkSampleReader instance
    2. Reads the first 5 samples from the CSV file
    3. Displays the samples in a formatted way
    4. Handles any errors that occur during execution
    """
    try:
        # Display author name at the start
        print("\n" + "="*80)
        print(f"Author: {AUTHOR_NAME}".center(80))
        print("="*80 + "\n")
        
        reader = MilkSampleReader()
        samples = reader.read_samples(6)  # Read first 5 samples
        
        # Display the samples in a formatted way
        reader.display_samples()
            
    except FileNotFoundError:
        print("Please ensure the CSV file is in the correct location.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 