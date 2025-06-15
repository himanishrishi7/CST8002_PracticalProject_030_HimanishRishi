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
        print("5. Create new sample")
        print("6. Edit existing sample")
        print("7. Exit")
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
    
    def handle_create_sample(self):
        """Handle creating a new milk sample record."""
        try:
            print("\nEnter sample details:")
            sample_type = input("Sample Type (e.g., MILK): ").strip()
            type = input("Type (e.g., WHOLE): ").strip()
            start_date = input("Start Date (YYYY-MM-DD): ").strip()
            stop_date = input("Stop Date (YYYY-MM-DD): ").strip()
            station_name = input("Station Name: ").strip()
            province = input("Province: ").strip()
            
            # Get Sr90 activity with validation
            while True:
                try:
                    sr90_activity = float(input("Sr90 Activity (Bq/L): ").strip())
                    if sr90_activity < 0:
                        print("Activity must be non-negative. Please try again.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")
            
            # Get optional fields
            sr90_error = None
            error_input = input("Sr90 Error (Bq/L) [optional, press Enter to skip]: ").strip()
            if error_input:
                try:
                    sr90_error = float(error_input)
                except ValueError:
                    print("Invalid error value. Skipping error field.")
            
            sr90_activity_per_calcium = None
            calcium_input = input("Sr90 Activity/Calcium (Bq/g) [optional, press Enter to skip]: ").strip()
            if calcium_input:
                try:
                    sr90_activity_per_calcium = float(calcium_input)
                except ValueError:
                    print("Invalid calcium value. Skipping calcium field.")
            
            # Create the new sample
            new_sample = self.service.create_new_sample(
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
            
            print("\nNew sample created successfully!")
            self.display_sample(new_sample, len(self.service.samples) - 1)
            
        except ValueError as e:
            print(f"\nError creating sample: {str(e)}")
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")
        print(f"Author: {AUTHOR_NAME}".center(80))
    
    def handle_edit_sample(self):
        """Handle editing an existing milk sample record."""
        try:
            # First, display all samples to help user choose
            print("\nAvailable samples:")
            self.display_all_samples()
            
            # Get sample index
            while True:
                try:
                    index = int(input("\nEnter the number of the sample to edit (1-{}): ".format(
                        self.service.get_sample_count()))) - 1
                    if 0 <= index < self.service.get_sample_count():
                        break
                    print("Invalid sample number. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Get current sample
            current_sample = self.service.get_sample(index)
            print("\nCurrent sample values:")
            self.display_sample(current_sample, index)
            
            print("\nEnter new values (press Enter to keep current value):")
            
            # Get new values for each field
            sample_type = input(f"Sample Type [{current_sample.sample_type}]: ").strip()
            type = input(f"Type [{current_sample.type}]: ").strip()
            start_date = input(f"Start Date [{current_sample.start_date}]: ").strip()
            stop_date = input(f"Stop Date [{current_sample.stop_date}]: ").strip()
            station_name = input(f"Station Name [{current_sample.station_name}]: ").strip()
            province = input(f"Province [{current_sample.province}]: ").strip()
            
            # Get Sr90 activity with validation
            while True:
                activity_input = input(f"Sr90 Activity (Bq/L) [{current_sample.sr90_activity}]: ").strip()
                if not activity_input:  # Keep current value
                    sr90_activity = current_sample.sr90_activity
                    break
                try:
                    sr90_activity = float(activity_input)
                    if sr90_activity < 0:
                        print("Activity must be non-negative. Please try again.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")
            
            # Get optional fields
            error_input = input(f"Sr90 Error (Bq/L) [{current_sample.sr90_error}]: ").strip()
            sr90_error = float(error_input) if error_input else current_sample.sr90_error
            
            calcium_input = input(f"Sr90 Activity/Calcium (Bq/g) [{current_sample.sr90_activity_per_calcium}]: ").strip()
            sr90_activity_per_calcium = float(calcium_input) if calcium_input else current_sample.sr90_activity_per_calcium
            
            # Update the sample
            old_sample, new_sample = self.service.edit_sample(
                index,
                sample_type=sample_type or current_sample.sample_type,
                type=type or current_sample.type,
                start_date=start_date or current_sample.start_date,
                stop_date=stop_date or current_sample.stop_date,
                station_name=station_name or current_sample.station_name,
                province=province or current_sample.province,
                sr90_activity=sr90_activity,
                sr90_error=sr90_error,
                sr90_activity_per_calcium=sr90_activity_per_calcium
            )
            
            print("\nSample updated successfully!")
            print("\nOld values:")
            self.display_sample(old_sample, index)
            print("\nNew values:")
            self.display_sample(new_sample, index)
            
        except ValueError as e:
            print(f"\nError updating sample: {str(e)}")
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")
        print(f"Author: {AUTHOR_NAME}".center(80))
    
    def run(self):
        """Run the main application loop."""
        try:
            self.display_header()
            while True:
                self.display_menu()
                choice = input("\nEnter your choice (1-7): ")
                
                if choice == "1":
                    self.handle_reload()
                elif choice == "2":
                    self.display_all_samples()
                elif choice == "3":
                    self.handle_display_single()
                elif choice == "4":
                    self.handle_save_samples()
                elif choice == "5":
                    self.handle_create_sample()
                elif choice == "6":
                    self.handle_edit_sample()
                elif choice == "7":
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