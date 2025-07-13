"""
Debug script to analyze CSV parsing issues
"""

import csv
import os
from src.model.milk_sample_record import MilkSampleRecord

def analyze_csv_file():
    """Analyze the CSV file to understand the parsing issues."""
    
    csv_filename = "nms_strontium90_milk_ssn_strontium90_lait.csv"
    csv_path = os.path.join(os.getcwd(), csv_filename)
    
    print(f"Analyzing CSV file: {csv_path}")
    print("="*60)
    
    total_rows = 0
    valid_rows = 0
    skipped_rows = 0
    error_rows = []
    
    try:
        with open(csv_path, "r", encoding="utf-8-sig", errors='ignore') as f:
            csv_reader = csv.reader(f)
            header = next(csv_reader)  # Get header
            print(f"Header: {header}")
            print(f"Header length: {len(header)}")
            print()
            
            for row_num, values in enumerate(csv_reader, start=2):
                total_rows += 1
                
                # Clean and validate values
                cleaned_values = [v.strip() for v in values if v.strip()]
                
                if len(cleaned_values) < 9:
                    print(f"Row {row_num}: Insufficient values (found {len(cleaned_values)}, need 9)")
                    print(f"  Raw values: {values}")
                    print(f"  Cleaned values: {cleaned_values}")
                    skipped_rows += 1
                    error_rows.append((row_num, "Insufficient values", values))
                    continue
                
                try:
                    record = MilkSampleRecord(
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
                    valid_rows += 1
                    
                    # Show first few successful records
                    if valid_rows <= 3:
                        print(f"Row {row_num}: Successfully parsed")
                        print(f"  Sample: {record.sample_type}, {record.type}, {record.station_name}, {record.province}")
                    
                except (ValueError, IndexError) as e:
                    print(f"Row {row_num}: Error parsing - {str(e)}")
                    print(f"  Raw values: {values}")
                    print(f"  Cleaned values: {cleaned_values}")
                    skipped_rows += 1
                    error_rows.append((row_num, str(e), values))
                    continue
                    
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return
    
    print("\n" + "="*60)
    print("ANALYSIS RESULTS:")
    print(f"Total rows in CSV: {total_rows}")
    print(f"Successfully parsed: {valid_rows}")
    print(f"Skipped/Error rows: {skipped_rows}")
    print(f"Success rate: {(valid_rows/total_rows)*100:.1f}%")
    
    if error_rows:
        print(f"\nFirst 10 error rows:")
        for i, (row_num, error, values) in enumerate(error_rows[:10]):
            print(f"  Row {row_num}: {error}")
            print(f"    Values: {values}")
            print()

def check_csv_structure():
    """Check the structure of the CSV file."""
    
    csv_filename = "nms_strontium90_milk_ssn_strontium90_lait.csv"
    csv_path = os.path.join(os.getcwd(), csv_filename)
    
    print(f"\nChecking CSV structure: {csv_path}")
    print("="*60)
    
    try:
        with open(csv_path, "r", encoding="utf-8-sig", errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            
            print(f"Total lines in file: {len(lines)}")
            print(f"Non-empty lines: {len([line for line in lines if line.strip()])}")
            
            # Check for empty lines or problematic lines
            empty_lines = []
            short_lines = []
            
            for i, line in enumerate(lines, 1):
                if not line.strip():
                    empty_lines.append(i)
                elif len(line.split(',')) < 9:
                    short_lines.append((i, line))
            
            print(f"Empty lines: {len(empty_lines)}")
            if empty_lines:
                print(f"  Empty line numbers: {empty_lines[:10]}{'...' if len(empty_lines) > 10 else ''}")
            
            print(f"Short lines (< 9 columns): {len(short_lines)}")
            if short_lines:
                print("  First few short lines:")
                for line_num, line in short_lines[:5]:
                    print(f"    Line {line_num}: {line}")
                    
    except Exception as e:
        print(f"Error checking CSV structure: {str(e)}")

if __name__ == "__main__":
    analyze_csv_file()
    check_csv_structure() 