"""
CST8002 - Practical Project 2
Professor: Tyler DeLay
Due Date: 25/05/2025
Author: Himanish Rishi

This module contains the MilkSampleView class which handles user interaction and
display of milk sample data. It is part of the Presentation Layer.
"""

from src.business.milk_sample_service import MilkSampleService
from src.business.milk_sample_record import MilkSampleRecord

class MilkSampleView:
    """
    A class to handle user interaction and display of milk sample data.
    
    This class is responsible for:
    1. Displaying sample data in a formatted way
    2. Handling user interaction
    3. Coordinating with the business layer
    """
    
    def __init__(self):
        """Initialize the view with a service instance."""
        self.service = MilkSampleService()
    
    def display_header(self):
        """Display the application header."""
        print("\n" + "="*80)
        print("MILK SAMPLE DATA VIEWER".center(80))
        print("="*80 + "\n")
    
    def display_sample(self, sample: MilkSampleRecord, index: int):
        """
        Display a single sample in a formatted way.
        
        Args:
            sample (MilkSampleRecord): The sample to display
            index (int): The sample's index
        """
        print(f"\nSample #{index + 1}")
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
    
    def display_all_samples(self):
        """Display all loaded samples."""
        samples = self.service.get_all_samples()
        for i, sample in enumerate(samples):
            self.display_sample(sample, i)
    
    def run(self):
        """Run the main application loop."""
        try:
            self.display_header()
            self.service.load_samples(6)
            self.display_all_samples()
        except Exception as e:
            print(f"An error occurred: {str(e)}")

def main():
    """Main entry point for the application."""
    view = MilkSampleView()
    view.run()

if __name__ == "__main__":
    main() 