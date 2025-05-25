import csv
from typing import List
from milk_sample import MilkSample

class MilkSampleReader:
    def __init__(self, filename: str = "nms_strontium90_milk_ssn_strontium90_lait (1).csv"):
        """
        Initialize the MilkSampleReader with the CSV file path.
        
        Args:
            filename (str): Path to the CSV file containing milk sample data
        """
        self.filename = filename
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
            with open(self.filename, 'r', encoding='utf-8') as file:
                # Skip header row
                next(file)
                
                # Read specified number of records
                for _ in range(num_samples):
                    try:
                        line = next(file)
                        # Split the line and remove any empty fields
                        values = [v.strip() for v in line.split(',') if v.strip()]
                        
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
                        print(f"Error parsing line: {line}")
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

def main():
    """Main function to demonstrate the MilkSampleReader functionality."""
    try:
        reader = MilkSampleReader()
        samples = reader.read_samples(5)  # Read first 5 samples
        
        print(f"\nSuccessfully read {len(samples)} samples:")
        for i, sample in enumerate(samples, 1):
            print(f"\nSample {i}:")
            print(sample)
            
    except FileNotFoundError:
        print("Please ensure the CSV file is in the correct location.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 