import csv
from typing import List
from milk_sample import MilkSample


# Author information
AUTHOR_NAME = "Himanish Rishi"
class MilkSampleReader:
    def __init__(self):
        """
        Initialize the MilkSampleReader with a hardcoded CSV file path.
        """
        self.filename = 'nms_strontium90_milk_ssn_strontium90_lait.csv'
        self.samples: List[MilkSample] = []

    def read_samples(self, num_samples: int = 5) -> List[MilkSample]:
        """
        Read the specified number of samples from the CSV file.
        
        Args:
            num_samples (int): Number of samples to read (default: 5)
            
        Returns:
            List[MilkSample]: List of MilkSample objects
            
        Raises:
            FileNotFoundError: If the CSV file is not found
            ValueError: If there's an error parsing the data
        """
        try:
            with open(self.filename, "r", encoding="utf-8-sig", errors='ignore') as f:
                csv_reader = csv.reader(f)
                # Skip header row
                next(csv_reader)
                
                # Read specified number of records
                for _ in range(num_samples):
                    try:
                        values = next(csv_reader)
                        # Remove any empty fields
                        values = [v.strip() for v in values if v.strip()]
                        
                        if len(values) >= 9:
                            # Create a new MilkSample object
                            sample = MilkSample(
                                sample_type=values[0],
                                type=values[1],
                                start_date=values[2],
                                stop_date=values[3],
                                station_name=values[4],
                                province=values[5],
                                sr90_activity=self._parse_float(values[6]),
                                sr90_error=self._parse_float(values[7]),
                                sr90_activity_per_calcium=self._parse_float(values[8])
                            )
                            self.samples.append(sample)
                    except StopIteration:
                        break
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing line: {values}")
                        print(f"Error details: {str(e)}")
                        continue
                        
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            raise
        except Exception as e:
            print(f"Unexpected error reading file: {str(e)}")
            raise
            
        return self.samples

    def _parse_float(self, value: str) -> float:
        """
        Parse a string value to float, handling scientific notation.
        
        Args:
            value (str): String value to parse
            
        Returns:
            float: Parsed float value or 0.0 if parsing fails
        """
        try:
            return float(value) if value else 0.0
        except ValueError:
            return 0.0

    def display_samples(self):
        """
        Display all samples in the data structure in a formatted way.
        """
        if not self.samples:
            print("No samples to display.")
            return

        print("\n" + "="*80)
        print(f"Author: {AUTHOR_NAME}".center(80))
        print("="*80)
        print("MILK SAMPLE DATA".center(80))
        print("="*80)

        for i, sample in enumerate(self.samples, 1):
            print(f"\nSample #{i}")
            print("-"*40)
            print(f"Sample Type: {sample.sample_type}")
            print(f"Type: {sample.type}")
            print(f"Date Range: {sample.start_date} to {sample.stop_date}")
            print(f"Location: {sample.station_name}, {sample.province}")
            print(f"Sr-90 Activity: {sample.sr90_activity:.2e} Bq/L")
            print(f"Sr-90 Error: {sample.sr90_error:.2e} Bq/L")
            print(f"Sr-90 Activity/Calcium: {sample.sr90_activity_per_calcium:.2e} Bq/g")
            print("-"*40)

def main():
    """Main function to demonstrate the MilkSampleReader functionality."""
    try:
        # Display author name at the start
        print("\n" + "="*80)
        print(f"Author: {AUTHOR_NAME}".center(80))
        print("="*80 + "\n")
        
        reader = MilkSampleReader()
        samples = reader.read_samples(5)  # Read first 5 samples
        
        # Display the samples in a formatted way
        reader.display_samples()
            
    except FileNotFoundError:
        print("Please ensure the CSV file is in the correct location.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 