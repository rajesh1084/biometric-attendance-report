#!/usr/bin/env python3
"""
Biometric Attendance Report Generator

This script generates PDF reports from biometric attendance data for specified date ranges.
It calculates late punches (after 9:15 AM) and early punches (before 4:15 PM) for each employee.

Usage:
    python attendance_report.py <input_file> <start_date> <end_date>

Arguments:
    input_file: Path to the CSV file containing attendance data
    start_date: Start date in YYYY-MM-DD format
    end_date: End date in YYYY-MM-DD format

Example:
    python attendance_report.py input/Biometric_Attendance_2025.csv 2025-01-01 2025-01-31
"""

import pandas as pd
import argparse
import sys
from datetime import datetime, time
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import os


def parse_time(time_str):
    """Parse time string in HH:MM format to time object."""
    if pd.isna(time_str) or time_str == '':
        return None
    try:
        return datetime.strptime(time_str.strip(), '%H:%M').time()
    except ValueError:
        return None


def is_late_punch(clock_in_time):
    """Check if clock in time is after 9:15 AM."""
    if clock_in_time is None:
        return False
    late_threshold = time(9, 15)  # 9:15 AM
    return clock_in_time > late_threshold


def is_early_punch(clock_out_time):
    """Check if clock out time is before 4:15 PM."""
    if clock_out_time is None:
        return False
    early_threshold = time(16, 15)  # 4:15 PM
    return clock_out_time < early_threshold


def load_and_filter_data(file_path, start_date, end_date):
    """Load CSV data and filter by date range."""
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Convert start_date and end_date to datetime
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        # Filter by date range
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        
        # Exclude rows where both Clock In and Clock Out are empty
        df = df[~(df['Clock In'].isna() & df['Clock Out'].isna())]
        df = df[~((df['Clock In'] == '') & (df['Clock Out'] == ''))]
        
        return df
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def calculate_attendance_summary(df):
    """Calculate late and early punch counts for each employee."""
    summary_data = []
    
    # Group by Employee ID and First Name
    grouped = df.groupby(['Employee ID', 'First Name'])
    
    for (emp_id, first_name), group in grouped:
        late_punch_count = 0
        early_punch_count = 0
        
        for _, row in group.iterrows():
            # Parse clock in and clock out times
            clock_in_time = parse_time(row['Clock In'])
            clock_out_time = parse_time(row['Clock Out'])
            
            # Count late punches
            if is_late_punch(clock_in_time):
                late_punch_count += 1
            
            # Count early punches
            if is_early_punch(clock_out_time):
                early_punch_count += 1
        
        summary_data.append({
            'Employee ID': emp_id,
            'First Name': first_name,
            'Total Late Punch': late_punch_count,
            'Total Early Punch': early_punch_count
        })
    
    return pd.DataFrame(summary_data)


def create_pdf_report(summary_df, start_date, end_date, output_file):
    """Create PDF report from summary data."""
    # Create the PDF document
    doc = SimpleDocTemplate(output_file, pagesize=A4)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Add title
    title = f"Attendance Report ({start_date} to {end_date})"
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 20))
    
    # Add report generation info
    report_info = f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    story.append(Paragraph(report_info, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Create table data
    table_data = [['Employee ID', 'First Name', 'Total Late Punch', 'Total Early Punch']]
    
    for _, row in summary_df.iterrows():
        table_data.append([
            str(row['Employee ID']),
            str(row['First Name']),
            str(row['Total Late Punch']),
            str(row['Total Early Punch'])
        ])
    
    # Create table
    table = Table(table_data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 1.5*inch])
    
    # Apply table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(table)
    
    # Add summary statistics
    story.append(Spacer(1, 30))
    summary_title = Paragraph("Summary Statistics", styles['Heading2'])
    story.append(summary_title)
    story.append(Spacer(1, 12))
    
    total_employees = len(summary_df)
    total_late_punches = summary_df['Total Late Punch'].sum()
    total_early_punches = summary_df['Total Early Punch'].sum()
    
    summary_text = f"""
    Total Employees: {total_employees}<br/>
    Total Late Punches: {total_late_punches}<br/>
    Total Early Punches: {total_early_punches}<br/>
    <br/>
    Note: Late punch is defined as any clock-in after 9:15 AM<br/>
    Early punch is defined as any clock-out before 4:15 PM
    """
    
    story.append(Paragraph(summary_text, styles['Normal']))
    
    # Build the PDF
    doc.build(story)
    print(f"PDF report generated: {output_file}")


def main():
    """Main function to parse arguments and generate report."""
    parser = argparse.ArgumentParser(
        description='Generate attendance report from biometric data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python attendance_report.py input/data.csv 2025-01-01 2025-01-31
  python attendance_report.py /path/to/attendance.csv 2025-06-01 2025-06-25
        """
    )
    
    parser.add_argument('input_file', help='Path to the CSV file containing attendance data')
    parser.add_argument('start_date', help='Start date in YYYY-MM-DD format')
    parser.add_argument('end_date', help='End date in YYYY-MM-DD format')
    
    args = parser.parse_args()
    
    # Validate date format
    try:
        datetime.strptime(args.start_date, '%Y-%m-%d')
        datetime.strptime(args.end_date, '%Y-%m-%d')
    except ValueError:
        print("Error: Dates must be in YYYY-MM-DD format")
        sys.exit(1)
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        sys.exit(1)
    
    print(f"Processing attendance data from {args.start_date} to {args.end_date}...")
    
    # Load and filter data
    df = load_and_filter_data(args.input_file, args.start_date, args.end_date)
    
    if df.empty:
        print("No data found for the specified date range.")
        sys.exit(1)
    
    print(f"Found {len(df)} attendance records in the date range.")
    
    # Calculate summary
    summary_df = calculate_attendance_summary(df)
    
    if summary_df.empty:
        print("No valid attendance data found after filtering.")
        sys.exit(1)
    
    print(f"Processed data for {len(summary_df)} employees.")
    
    # Generate output filename
    output_file = f"attendance_report_{args.start_date}_to_{args.end_date}.pdf"
    
    # Create PDF report
    create_pdf_report(summary_df, args.start_date, args.end_date, output_file)
    
    print("\nReport Summary:")
    print(f"Total Employees: {len(summary_df)}")
    print(f"Total Late Punches: {summary_df['Total Late Punch'].sum()}")
    print(f"Total Early Punches: {summary_df['Total Early Punch'].sum()}")


if __name__ == "__main__":
    main()
