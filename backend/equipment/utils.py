"""
Utility functions for CSV parsing and analytics.
Uses Pandas for reliable data processing.
"""
import pandas as pd
from io import StringIO


# CRITICAL: These are the EXACT column names required
REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']


def validate_csv_structure(file):
    """
    Validates that CSV has required columns.
    Returns (is_valid, error_message)
    """
    try:
        # Read CSV
        df = pd.read_csv(file)
        
        # Check for required columns
        missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Check for numeric columns
        numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
        for col in numeric_columns:
            if not pd.to_numeric(df[col], errors='coerce').notna().all():
                return False, f"Column '{col}' must contain only numeric values"
        
        return True, None
    
    except Exception as e:
        return False, f"Error reading CSV: {str(e)}"


def analyze_csv(file):
    """
    Analyzes uploaded CSV and returns summary statistics.
    
    Returns:
        tuple: (summary_dict, raw_data_list)
    """
    # Read CSV with Pandas
    df = pd.read_csv(file)
    
    # Calculate summary statistics
    summary = {
        "total_equipment": int(len(df)),
        "average_flowrate": float(df["Flowrate"].mean()),
        "average_pressure": float(df["Pressure"].mean()),
        "average_temperature": float(df["Temperature"].mean()),
        "type_distribution": df["Type"].value_counts().to_dict(),
        
        # Additional statistics for better insights
        "min_flowrate": float(df["Flowrate"].min()),
        "max_flowrate": float(df["Flowrate"].max()),
        "min_pressure": float(df["Pressure"].min()),
        "max_pressure": float(df["Pressure"].max()),
        "min_temperature": float(df["Temperature"].min()),
        "max_temperature": float(df["Temperature"].max()),
    }
    
    # Convert DataFrame to list of dictionaries for storage
    raw_data = df.to_dict(orient="records")
    
    return summary, raw_data


def get_chart_data(summary):
    """
    Formats summary data for frontend charts.
    
    Returns:
        dict: Chart-ready data structure
    """
    return {
        "type_distribution": {
            "labels": list(summary["type_distribution"].keys()),
            "values": list(summary["type_distribution"].values())
        },
        "averages": {
            "flowrate": summary["average_flowrate"],
            "pressure": summary["average_pressure"],
            "temperature": summary["average_temperature"]
        }
    }
