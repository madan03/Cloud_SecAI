import pandas as pd
import os

# Define paths
input_file_path = '../output/aws/prowler_results.csv'
output_directory = 'output_pre'
output_file_path = os.path.join(output_directory, 'prowler_aggregated_severity_counts.csv')

# Create the output directory if it does not exist
os.makedirs(output_directory, exist_ok=True)

# Load data with semicolon as delimiter, skip rows with format issues
data = pd.read_csv(input_file_path, on_bad_lines='skip', delimiter=';')

# Define relevant columns based on expected structure
relevant_columns = ['SERVICE_NAME', 'STATUS', 'SEVERITY', 'TIMESTAMP']

# Check if all relevant columns are present before proceeding
if all(col in data.columns for col in relevant_columns):
    # Filter data by relevant columns
    data = data[relevant_columns].copy()

    # Convert TIMESTAMP to  and drop rows with invalid dates
    data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'], errors='coerce')
    data.dropna(subset=['TIMESTAMP'], inplace=True)

    # Fill missing values in categorical fields with "Unknown"
    data = data.fillna({'SERVICE_NAME': 'Unknown', 'STATUS': 'Unknown', 'SEVERITY': 'Unknown'})

    # Standardize text fields to lowercase to ensure consistency
    data['SERVICE_NAME'] = data['SERVICE_NAME'].str.lower().str.strip()
    data['STATUS'] = data['STATUS'].str.lower().str.strip()

    # Aggregate severity counts by timestamp and service name
    severity_counts = data.pivot_table(
        index=['TIMESTAMP', 'SERVICE_NAME'],
        columns='SEVERITY',
        aggfunc='size',
        fill_value=0
    ).reset_index()

    # Rename columns for clarity
    severity_counts.columns.name = None
    severity_counts = severity_counts.rename(columns={
        'low': 'Low', 
        'medium': 'Medium', 
        'high': 'High', 
        'critical': 'Critical'
    })

    # Optional: Add derived fields like total findings or severity score
    severity_counts['total_findings'] = (
        severity_counts['Critical'] * 3 +
        severity_counts['High'] * 2 +
        severity_counts['Medium'] * 1 +
        severity_counts['Low'] * 0.5
    )

    # Save to CSV
    severity_counts.to_csv(output_file_path, index=False)
    print(f"Aggregated data saved to {output_file_path}")
else:
    print("Required columns not found. Please verify the CSV structure.")
