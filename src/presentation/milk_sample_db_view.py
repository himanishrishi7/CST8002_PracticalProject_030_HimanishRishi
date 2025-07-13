"""
CST8002 - Practical Project 3
Professor: Tyler DeLay
Due Date: 25/05/2025
Author: Himanish Rishi

This module contains the MilkSampleDBView class which handles user interaction and
display of milk sample data using database operations. It is part of the Presentation Layer.

This version uses the database service instead of file-based operations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.business.milk_sample_db_service import MilkSampleDBService
from src.model.milk_sample_record import MilkSampleRecord
from src.persistence.data_migration import DataMigration
from src.persistence.database_config import DatabaseConfig

# Author information
AUTHOR_NAME = "Himanish Rishi"

class MilkSampleDBView:
    """
    A class to handle user interaction and display of milk sample data using database operations.
    
    This class is responsible for:
    1. Displaying sample data in a formatted way
    2. Handling user interaction
    3. Coordinating with the database business layer
    4. Managing database operations
    """
    
    def __init__(self):
        """Initialize the view with a database service instance."""
        self.service = MilkSampleDBService()
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize the database by clearing existing data and reloading from CSV."""
        try:
            print("Initializing database...")
            
            # Close all database connections more aggressively
            try:
                if hasattr(self.service.repository, 'db_config'):
                    self.service.repository.db_config.close_connection()
                if hasattr(self.service, 'repository') and hasattr(self.service.repository, 'db_config'):
                    self.service.repository.db_config.close_connection()
            except Exception as e:
                print(f"Warning: Could not close some connections: {e}")
            
            # Force garbage collection to release file handles
            import gc
            gc.collect()
            
            # More aggressive approach: Delete and recreate database file
            db_config = DatabaseConfig()
            if os.path.exists(db_config.db_path):
                print(f"Removing existing database file: {db_config.db_path}")
                try:
                    os.remove(db_config.db_path)
                    print("Database file removed successfully")
                except PermissionError:
                    print("Warning: Could not delete database file (may be in use). Continuing with existing file.")
                except Exception as e:
                    print(f"Warning: Error deleting database file: {e}. Continuing with existing file.")
            
            # Create fresh database and table
            print("Creating fresh database...")
            db_config.initialize_database()
            
            # Always clear existing data first (in case there's any)
            migration = DataMigration()
            print("Clearing existing database records...")
            migration.db_repository.clear_all_samples()
            
            # Reload fresh data from CSV
            print("Migrating fresh data from CSV...")
            total, successful, failed = migration.migrate_data()
            print(f"Migration completed: {successful} records imported")
            
            # Verify the data
            count = self.service.get_sample_count()
            print(f"Database now contains {count} records")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def display_header(self):
        """Display the application header with author information."""
        print("\n" + "="*80)
        print(f"Program by {AUTHOR_NAME}".center(80))
        print("="*80)
        print("MILK SAMPLE DATA VIEWER (DATABASE VERSION)".center(80))
        print("="*80 + "\n")
    
    def display_menu(self):
        """Display the main menu options."""
        print("\nMain Menu:")
        print("1. Reload data from CSV to database")
        print("2. Display all samples")
        print("3. Display a single sample by ID")
        print("4. Display samples by province")
        print("5. Display samples by station")
        print("6. Create new sample")
        print("7. Edit existing sample")
        print("8. Delete sample")
        print("9. Show database statistics")
        print("10. Exit")
        print("-"*40)
        print(f"Program by {AUTHOR_NAME}".center(80))
    
    def display_sample(self, sample: MilkSampleRecord, sample_id: int = None):
        """
        Display a single sample in a formatted way.
        
        Args:
            sample (MilkSampleRecord): The sample to display
            sample_id (int): The sample's database ID (optional)
        """
        if sample_id is not None:
            print(f"\nSample ID: {sample_id}")
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
        print(f"Program by {AUTHOR_NAME}".center(80))
    
    def display_all_samples(self):
        """Display all samples from database."""
        try:
            samples_with_ids = self.service.get_all_samples_with_ids(limit=50)  # Limit to first 50 for display
            print(f"\nDisplaying first {len(samples_with_ids)} samples from database:")
            for record_id, sample in samples_with_ids:
                self.display_sample(sample, record_id)  # Use actual database ID
                if record_id % 5 == 0:  # Add separator every 5 samples
                    print("\n" + "="*80)
                    print(f"Program by {AUTHOR_NAME}".center(80))
                    print("="*80 + "\n")
        except Exception as e:
            print(f"Error displaying samples: {e}")
    
    def handle_reload(self):
        """Handle reloading data from CSV to database with aggressive refresh."""
        try:
            print("\nReloading data from CSV to database...")
            
            # Close all database connections more aggressively
            try:
                if hasattr(self.service.repository, 'db_config'):
                    self.service.repository.db_config.close_connection()
                if hasattr(self.service, 'repository') and hasattr(self.service.repository, 'db_config'):
                    self.service.repository.db_config.close_connection()
            except Exception as e:
                print(f"Warning: Could not close some connections: {e}")
            
            # Force garbage collection to release file handles
            import gc
            gc.collect()
            
            # More aggressive approach: Delete and recreate database file
            db_config = DatabaseConfig()
            if os.path.exists(db_config.db_path):
                print(f"Removing existing database file: {db_config.db_path}")
                try:
                    os.remove(db_config.db_path)
                    print("Database file removed successfully")
                except PermissionError:
                    print("Warning: Could not delete database file (may be in use). Continuing with existing file.")
                except Exception as e:
                    print(f"Warning: Error deleting database file: {e}. Continuing with existing file.")
            
            # Create fresh database and table
            print("Creating fresh database...")
            db_config.initialize_database()
            
            # Always clear existing data first (in case there's any)
            migration = DataMigration()
            print("Clearing existing database records...")
            migration.db_repository.clear_all_samples()
            
            # Reload fresh data from CSV
            print("Migrating fresh data from CSV...")
            total, successful, failed = migration.migrate_data()
            print(f"Migration completed: {successful} records imported")
            
            # Verify the data
            count = self.service.get_sample_count()
            print(f"Database now contains {count} records")
            
        except Exception as e:
            print(f"Error reloading data: {str(e)}")
        print(f"Program by {AUTHOR_NAME}".center(80))
    
    def handle_display_single(self):
        """Handle displaying a single sample by ID."""
        try:
            sample_id = int(input("\nEnter sample ID: "))
            sample = self.service.get_sample_by_id(sample_id)
            if sample:
                self.display_sample(sample, sample_id)
            else:
                print("Sample not found.")
        except ValueError:
            print("Please enter a valid ID number.")
        print(f"Program by {AUTHOR_NAME}".center(80))
    
    def handle_display_by_province(self):
        """Handle displaying samples by province."""
        try:
            provinces = self.service.get_available_provinces()
            print(f"\nAvailable provinces: {', '.join(provinces)}")
            province = input("Enter province name: ").strip()
            
            if province in provinces:
                samples = self.service.get_samples_by_province(province)
                print(f"\nFound {len(samples)} samples from {province}:")
                for i, sample in enumerate(samples, 1):
                    self.display_sample(sample, i)
            else:
                print("Province not found.")
        except Exception as e:
            print(f"Error displaying samples by province: {e}")
        print(f"Program by {AUTHOR_NAME}".center(80))
    
    def handle_display_by_station(self):
        """Handle displaying samples by station."""
        try:
            stations = self.service.get_available_stations()
            print(f"\nAvailable stations: {', '.join(stations)}")
            station = input("Enter station name: ").strip()
            
            if station in stations:
                samples = self.service.get_samples_by_station(station)
                print(f"\nFound {len(samples)} samples from {station}:")
                for i, sample in enumerate(samples, 1):
                    self.display_sample(sample, i)
            else:
                print("Station not found.")
        except Exception as e:
            print(f"Error displaying samples by station: {e}")
        print(f"Program by {AUTHOR_NAME}".center(80))
    
    def handle_create_sample(self):
        """Handle creating a new milk sample record."""
        try:
            print("\nEnter sample details:")
            sample_type = input("Sample Type (e.g., MILK): ").strip()
            type = input("Type (e.g., WHOLE): ").strip()
            start_date = input("Start Date (e.g., 01-Jan-24): ").strip()
            stop_date = input("Stop Date (e.g., 31-Jan-24): ").strip()
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
            record_id, new_sample = self.service.create_new_sample(
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
            
            print(f"\nNew sample created successfully with ID: {record_id}!")
            self.display_sample(new_sample, record_id)
            
        except ValueError as e:
            print(f"\nError creating sample: {str(e)}")
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")
        print(f"Program by {AUTHOR_NAME}".center(80))
    
    def handle_edit_sample(self):
        """Handle editing an existing milk sample record."""
        try:
            sample_id = int(input("\nEnter the ID of the sample to edit: "))
            
            # Get current sample
            current_sample = self.service.get_sample_by_id(sample_id)
            if not current_sample:
                print("Sample not found.")
                return
                
            print("\nCurrent sample values:")
            self.display_sample(current_sample, sample_id)
            
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
            success, old_sample, new_sample = self.service.edit_sample(
                sample_id,
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
            
            if success:
                print("\nSample updated successfully!")
                print("\nOld values:")
                self.display_sample(old_sample, sample_id)
                print("\nNew values:")
                self.display_sample(new_sample, sample_id)
            else:
                print("Failed to update sample.")
            
        except ValueError as e:
            print(f"\nError updating sample: {str(e)}")
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")
        print(f"Program by {AUTHOR_NAME}".center(80))
    
    def handle_delete_sample(self):
        """Handle deleting a milk sample record."""
        try:
            sample_id = int(input("\nEnter the ID of the sample to delete: "))
            
            # Get sample to be deleted
            sample_to_delete = self.service.get_sample_by_id(sample_id)
            if not sample_to_delete:
                print("Sample not found.")
                return
                
            print("\nSample to be deleted:")
            self.display_sample(sample_to_delete, sample_id)
            
            # Confirm deletion
            confirm = input("\nAre you sure you want to delete this sample? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("\nDeletion cancelled.")
                return
            
            # Delete the sample
            success, deleted_sample = self.service.delete_sample(sample_id)
            if success:
                print("\nSample deleted successfully!")
                print("\nDeleted sample details:")
                self.display_sample(deleted_sample, sample_id)
                print(f"\nRemaining samples: {self.service.get_sample_count()}")
            else:
                print("Failed to delete sample.")
            
        except ValueError as e:
            print(f"\nError deleting sample: {str(e)}")
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")
        print(f"Program by {AUTHOR_NAME}".center(80))
    
    def handle_show_statistics(self):
        """Handle showing database statistics."""
        try:
            stats = self.service.get_statistics()
            print("\nDatabase Statistics:")
            print("-"*40)
            print(f"Total samples: {stats['total_samples']}")
            print(f"Unique provinces: {stats['unique_provinces']}")
            print(f"Unique stations: {stats['unique_stations']}")
            print(f"Average Sr90 activity: {stats['average_sr90_activity']:.6f} Bq/L")
            print(f"Valid activity readings: {stats['valid_activity_readings']}")
            print("\nProvinces:", ', '.join(stats['provinces']))
            print("\nStations:", ', '.join(stats['stations'][:10]) + "..." if len(stats['stations']) > 10 else ', '.join(stats['stations']))
        except Exception as e:
            print(f"Error showing statistics: {e}")
        print(f"Program by {AUTHOR_NAME}".center(80))
    
    def run(self):
        """Run the main application loop."""
        try:
            self.display_header()
            while True:
                self.display_menu()
                choice = input("\nEnter your choice (1-10): ")
                
                if choice == "1":
                    self.handle_reload()
                elif choice == "2":
                    self.display_all_samples()
                elif choice == "3":
                    self.handle_display_single()
                elif choice == "4":
                    self.handle_display_by_province()
                elif choice == "5":
                    self.handle_display_by_station()
                elif choice == "6":
                    self.handle_create_sample()
                elif choice == "7":
                    self.handle_edit_sample()
                elif choice == "8":
                    self.handle_delete_sample()
                elif choice == "9":
                    self.handle_show_statistics()
                elif choice == "10":
                    print("\nThank you for using the Milk Sample Data Viewer!")
                    print(f"Program by {AUTHOR_NAME}".center(80))
                    break
                else:
                    print("Invalid choice. Please try again.")
                    print(f"Program by {AUTHOR_NAME}".center(80))
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print(f"Program by {AUTHOR_NAME}".center(80))

def main():
    """Main entry point for the application."""
    view = MilkSampleDBView()
    view.run()

if __name__ == "__main__":
    main() 