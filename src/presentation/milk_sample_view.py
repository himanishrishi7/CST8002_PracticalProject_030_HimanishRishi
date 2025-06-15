"""
CST8002 - Practical Project 2
Professor: Tyler DeLay
Due Date: 25/05/2025
Author: Himanish Rishi

This module contains the MilkSampleView class which handles user interaction and
display of milk sample data. It is part of the Presentation Layer.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.business.milk_sample_service import MilkSampleService
from src.business.milk_sample_record import MilkSampleRecord

# Author information
AUTHOR_NAME = "Himanish Rishi"

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
        """Display the application header with author information."""
        print("\n" + "="*80)
        print(f"Author: {AUTHOR_NAME}".center(80))
        print("="*80)
        print("MILK SAMPLE DATA VIEWER".center(80))
        print("="*80 + "\n")
    
    def display_menu(self):
        """Display the main menu options."""
        print("\nMain Menu:")
        print("1. Reload data from dataset")
        print("2. Display all samples")
        print("3. Display a single sample")
        print("4. Save samples to new file")
        print("5. Exit")
        print("-"*40)
        print(f"Author: {AUTHOR_NAME}".center(80))
    
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
        print(f"Author: {AUTHOR_NAME}".center(80))
    
    def display_all_samples(self):
        """Display all loaded samples."""
        samples = self.service.get_all_samples()
        for i, sample in enumerate(samples):
            self.display_sample(sample, i)
    
    def handle_reload(self):
        """Handle reloading data from the dataset."""
        try:
            print("\nReloading data from dataset...")
            self.service.reload_samples(100)
            print(f"Successfully reloaded {self.service.get_sample_count()} samples.")
        except Exception as e:
            print(f"Error reloading data: {str(e)}")
        print(f"Author: {AUTHOR_NAME}".center(80))
    
    def handle_display_single(self):
        """Handle displaying a single sample."""
        try:
            index = int(input("\nEnter sample number (1-100): ")) - 1
            sample = self.service.get_sample(index)
            if sample:
                self.display_sample(sample, index)
            else:
                print("Invalid sample number.")
        except ValueError:
            print("Please enter a valid number.")
        print(f"Author: {AUTHOR_NAME}".center(80))
    
    def handle_save_samples(self):
        """Handle saving samples to a new file."""
        try:
            output_path = self.service.save_samples_to_new_file()
            print(f"\nSamples have been saved to: {output_path}")
        except Exception as e:
            print(f"\nError saving samples: {str(e)}")
        print(f"Author: {AUTHOR_NAME}".center(80))
    
    def run(self):
        """Run the main application loop."""
        try:
            self.display_header()
            while True:
                self.display_menu()
                choice = input("\nEnter your choice (1-5): ")
                
                if choice == "1":
                    self.handle_reload()
                elif choice == "2":
                    self.display_all_samples()
                elif choice == "3":
                    self.handle_display_single()
                elif choice == "4":
                    self.handle_save_samples()
                elif choice == "5":
                    print("\nThank you for using the Milk Sample Data Viewer!")
                    print(f"Author: {AUTHOR_NAME}".center(80))
                    break
                else:
                    print("Invalid choice. Please try again.")
                    print(f"Author: {AUTHOR_NAME}".center(80))
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print(f"Author: {AUTHOR_NAME}".center(80))

def main():
    """Main entry point for the application."""
    view = MilkSampleView()
    view.run()

if __name__ == "__main__":
    main() 