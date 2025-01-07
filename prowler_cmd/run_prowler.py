import subprocess
import os
from datetime import datetime
import glob
import shutil

def run_prowler_check():
    """Runs the Prowler command to execute check0 and appends output to prowler_results.csv."""
    # Define base output path
    base_output_path = os.path.join(os.getcwd(), "output")
    aws_output_path = os.path.join(base_output_path, "aws")

    # Create the AWS output directory if it doesn't exist
    os.makedirs(aws_output_path, exist_ok=True)

    # Define the main output file path
    output_file_path = os.path.join(aws_output_path, "prowler_results.csv")

    try:
        # Run the initial Prowler check and capture the output
        result = subprocess.run(
            ["prowler", "-c", "check0"],
            capture_output=True,
            text=True,
            check=True
        )
        print("Prowler check0 completed successfully.")
        
        # Run Prowler to generate a unique CSV output in aws directory
        subprocess.run(["prowler", "-M", "csv", "-o", aws_output_path])

        # Find the most recent Prowler output file in the aws directory
        latest_file = max(glob.glob(os.path.join(aws_output_path, "prowler-output-*.csv")), key=os.path.getctime)
        
        # Check if prowler_results.csv exists
        if not os.path.exists(output_file_path):
            # If prowler_results.csv doesn't exist, move the latest file as the base file
            shutil.move(latest_file, output_file_path)
            print(f"Prowler output saved successfully to {output_file_path}")
        else:
            # If prowler_results.csv exists, append the new results without the header
            with open(latest_file, 'r') as src, open(output_file_path, 'a') as dest:
                next(src)  # Skip the header row in the latest file
                shutil.copyfileobj(src, dest)
            print(f"Prowler output appended successfully to {output_file_path}")

        # Remove the unique generated file after appending or moving it
        if os.path.exists(latest_file):
            os.remove(latest_file)

        # Remove the compliance folder if it exists
        compliance_path = os.path.join(aws_output_path, "compliance")
        if os.path.exists(compliance_path):
            shutil.rmtree(compliance_path)
            print(f"Removed compliance directory at {compliance_path}")

    except subprocess.CalledProcessError as e:
        # Capture current timestamp for the error message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
        error_output = e.stderr if e.stderr else ""
        
        # Check for NoCredentialsError in the stderr output
        if "NoCredentialsError" in error_output or "Unable to locate credentials" in error_output:
            print(" //// Please login to AWS with admin-privilege credentials. ///////")
            print(f"An error occurred while running Prowler: Command '['prowler', '-c', 'check0']' returned non-zero exit status 1.")
        else:
            # Print other errors if they occur
            print(f"An error occurred while running Prowler: {e}")
            print(f"Error output:\n{error_output}")
    except FileNotFoundError:
        print("Prowler command not found. Ensure Prowler is installed and in PATH.")
