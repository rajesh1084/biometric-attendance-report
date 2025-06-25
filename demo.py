#!/usr/bin/env python3
"""
Demo script showing how to use the attendance report generator
"""

import subprocess
import sys
import os


def demo():
    """Run demonstration of the attendance report generator."""
    print("🎯 Biometric Attendance Report Generator Demo")
    print("=" * 50)

    # Check if input file exists
    input_file = "input/Biometric_Attendance_2025.csv"
    if not os.path.exists(input_file):
        print(f"❌ Demo input file not found: {input_file}")
        return

    print(f"📁 Using input file: {input_file}")
    print(f"📊 Analyzing attendance data...\n")

    # Demo 1: January 2025 report
    print("📋 Demo 1: Generating report for January 2025")
    print("-" * 40)

    try:
        result = subprocess.run(
            [
                sys.executable,
                "attendance_report.py",
                input_file,
                "2025-01-01",
                "2025-01-31",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ January report generated successfully!")
            print(result.stdout)
        else:
            print("❌ Error generating January report:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Exception: {e}")

    print("\n" + "=" * 50)

    # Demo 2: Weekly report
    print("📋 Demo 2: Generating report for a week in June 2025")
    print("-" * 40)

    try:
        result = subprocess.run(
            [
                sys.executable,
                "attendance_report.py",
                input_file,
                "2025-06-16",
                "2025-06-22",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ Weekly report generated successfully!")
            print(result.stdout)
        else:
            print("❌ Error generating weekly report:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Exception: {e}")

    print("\n" + "=" * 50)
    print("🎉 Demo completed!")

    # List generated files
    pdf_files = [f for f in os.listdir(".") if f.endswith(".pdf")]
    if pdf_files:
        print(f"\n📄 Generated PDF reports:")
        for pdf in pdf_files:
            print(f"   • {pdf}")

    print("\n💡 Usage Examples:")
    print("   python attendance_report.py input/data.csv 2025-01-01 2025-01-31")
    print("   python attendance_report.py input/data.csv 2025-06-01 2025-06-30")
    print("\n🔍 Features:")
    print("   • Late punch detection (after 9:15 AM)")
    print("   • Early punch detection (before 4:15 PM)")
    print("   • Professional PDF reports with statistics")
    print("   • Date range filtering")
    print("   • Command line interface")


if __name__ == "__main__":
    demo()
