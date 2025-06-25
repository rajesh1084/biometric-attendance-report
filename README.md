# Biometric Attendance Report Generator

A Python application that generates PDF reports from biometric attendance data, calculating late and early punch time in minutes for employees within a specified date range.

## Features

- **Date Range Filtering**: Generate reports for any specified date range
- **Late Punch Calculation**: Calculates minutes late after 9:15 AM for clock-ins
- **Early Punch Calculation**: Calculates minutes early before 4:15 PM for clock-outs
- **PDF Report Generation**: Creates professional PDF reports with summary statistics
- **Data Validation**: Excludes invalid entries where both clock-in and clock-out are empty
- **Command Line Interface**: Easy to use CLI with proper argument validation

## Requirements

- Python 3.6 or higher
- pandas >= 1.5.0
- reportlab >= 3.6.0

## Installation

1. Clone this repository:
```bash
git clone https://github.com/rajesh1084/biometric-attendance-report.git
cd biometric-attendance-report
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python attendance_report.py <input_file> <start_date> <end_date>
```

### Parameters

- `input_file`: Path to the CSV file containing attendance data
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format

### Examples

Generate a report for January 2025:
```bash
python attendance_report.py input/Biometric_Attendance_2025.csv 2025-01-01 2025-01-31
```

Generate a report for a specific week:
```bash
python attendance_report.py input/Biometric_Attendance_2025.csv 2025-06-01 2025-06-07
```

## Input Data Format

The input CSV file should contain the following columns:
- `Employee ID`: Unique identifier for each employee
- `First Name`: Employee's first name
- `Date`: Date in YYYY-MM-DD format
- `Clock In`: Clock-in time in HH:MM format
- `Clock Out`: Clock-out time in HH:MM format

### Sample Input Data
```csv
Employee ID,First Name,Department,Date,Timetable,Duration,Clock In,Clock Out,Actual WT,Total OT,Normal OT,Week Off OT,Holiday OT,Total WT,Status,Remarks
MRIT001,JOHN DOE,IT,2025-01-01,General Time Table,07:25,08:45,17:00,08:15,,,,,07:25,Present(P),
MRIT001,JOHN DOE,IT,2025-01-02,General Time Table,07:25,09:30,16:00,06:30,,,,,06:30,Present(P),
```

## Output

The application generates:

1. **PDF Report**: A professionally formatted PDF file with:
   - Report title with date range
   - Employee-wise summary table showing:
     - Employee ID
     - First Name
     - Total Late Punch Minutes
     - Total Early Punch Minutes
   - Summary statistics
   - Generation timestamp

2. **Console Output**: Summary information including:
   - Number of records processed
   - Number of employees
   - Total late and early minutes

### Sample Output File
The output file will be named: `attendance_report_YYYY-MM-DD_to_YYYY-MM-DD.pdf`

## Business Rules

- **Late Punch**: Minutes late after 9:15 AM for each clock-in
- **Early Punch**: Minutes early before 4:15 PM for each clock-out
- **Data Exclusion**: Days where both Clock In and Clock Out are empty are excluded from analysis
- **Date Range**: Only records within the specified date range are processed

## Error Handling

The application handles various error scenarios:
- Missing input files
- Invalid date formats
- Empty datasets
- Corrupted CSV files
- Invalid time formats

## Project Structure

```
biometric-attendance-report/
├── attendance_report.py      # Main application script
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── input/                   # Sample input directory
│   └── Biometric_Attendance_2025.csv
└── .gitignore              # Git ignore file
```

## Dependencies

### pandas
Used for:
- Reading and processing CSV files
- Data filtering and manipulation
- Date/time operations
- Grouping and aggregation

### reportlab
Used for:
- PDF document generation
- Table creation and styling
- Text formatting and layout
- Professional report formatting

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the existing issues on GitHub
2. Create a new issue with detailed description
3. Include sample data and error messages if applicable

## Version History

- **v1.0.0**: Initial release with basic functionality
  - Date range filtering
  - Late/early punch detection
  - PDF report generation
  - Command line interface
