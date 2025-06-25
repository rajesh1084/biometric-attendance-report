#!/usr/bin/env python3
"""
Test script for attendance report generator
"""

import subprocess
import sys
import os

def run_test():
    """Run a test with sample data."""
    input_file = "input/Biometric_Attendance_2025.csv"
    start_date = "2025-01-01"
    end_date = "2025-01-31"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        print("Please ensure the input file exists before running the test.")
        return False
    
    print("Running test with sample data...")
    print(f"Input file: {input_file}")
    print(f"Date range: {start_date} to {end_date}")
    
    try:
        # Run the attendance report script
        result = subprocess.run([
            sys.executable, "attendance_report.py", 
            input_file, start_date, end_date
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("\n✅ Test completed successfully!")
            print("Output:")
            print(result.stdout)
            
            # Check if PDF was generated
            expected_pdf = f"attendance_report_{start_date}_to_{end_date}.pdf"
            if os.path.exists(expected_pdf):
                print(f"✅ PDF report generated: {expected_pdf}")
                return True
            else:
                print(f"❌ PDF report not found: {expected_pdf}")
                return False
        else:
            print("❌ Test failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
