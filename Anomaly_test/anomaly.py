import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve Slack Webhook URL and API token from environment variables
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')
    SLACK_API_TOKEN = os.getenv('SLACK_API_TOKEN')  # Add your Slack API token to the .env file

    if not SLACK_API_TOKEN:
        print("Slack API token is missing. Please add it to the .env file.")
        exit(1)

    # Suppress chained assignment warnings
    pd.options.mode.chained_assignment = None

    # Define base paths
    base_dir = Path(__file__).resolve().parent.parent
    input_file_path = base_dir / 'DataPre/output_pre/prowler_aggregated_severity_counts.csv'
    output_dir = base_dir / 'Anomaly_test'
    output_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

    # Load preprocessed data
    if input_file_path.exists():
        data = pd.read_csv(input_file_path)
    else:
        print(f"The file was not found at {input_file_path}. Please check the path and try again.")
        exit(1)  # Exit the script if the file is not found

    # Feature Engineering: Create features for anomaly detection
    data['total_failures'] = data[['Critical', 'High', 'Medium', 'Low']].sum(axis=1)  # Total failures
    features = data[['total_failures', 'Critical', 'High', 'Medium', 'Low']]  # Features for modeling

    # Initialize and train Isolation Forest model
    isolation_forest = IsolationForest(contamination=0.05, random_state=42)  # 5% of data points are anomalies
    data['anomaly'] = isolation_forest.fit_predict(features)  # -1 indicates an anomaly, 1 is normal

    # Identify anomalies
    anomalies = data[data['anomaly'] == -1]

    # Function to send anomaly report and plot to Slack
    def send_anomaly_report_to_slack(anomalies, plot_path):
        if anomalies.empty:
            print("No anomalies detected.")
            return False  # No anomalies detected to send

        # Prepare the message in table format
        header = "*Anomaly Detection Report in Prowler Scan Results* :rotating_light:\n\n"
        table_header = "*Timestamp* | *Service Name* | *Total Failures* | *Critical* | *High* | *Medium* | *Low*\n"
        table_divider = "----------- | ------------- | ----------------- | --------- | ------ | -------- | ------\n"

        table_rows = ""
        for _, row in anomalies.iterrows():
            table_rows += f"{row['TIMESTAMP']} | {row['SERVICE_NAME']} | {row['total_failures']} | {row['Critical']} | {row['High']} | {row['Medium']} | {row['Low']}\n"

        message_text = header + table_header + table_divider + table_rows

        # Send the message text to Slack using Webhook URL
        message = {"text": message_text}
        response = requests.post(SLACK_WEBHOOK_URL, json=message)

        if response.status_code != 200:
            print(f"Failed to send message to Slack: {response.status_code} - {response.text}")
            return False

        # Step 1: Upload the file directly using files.upload
        try:
            with open(plot_path, 'rb') as file:
                upload_response = requests.post(
                    "https://slack.com/api/files.upload",
                    headers={"Authorization": f"Bearer {SLACK_API_TOKEN}"},
                    files={"file": file},
                    data={
                        "channels": "C081802DX1P",  # Replace with your Slack channel ID
                        "filename": os.path.basename(plot_path),
                        "title": "Anomaly Detection Plot",
                        "initial_comment": "Here is the anomaly detection plot for the latest scan."
                    }
                )

            upload_response_data = upload_response.json()

            if not upload_response_data.get('ok'):
                print(f"Slack API error during file upload: {upload_response_data.get('error')}")
                return False

            print("Plot image uploaded successfully to Slack.")
            return True

        except Exception as e:
            print(f"Error during file upload: {e}")
            return False

    # Plot total_failures over time, marking anomalies, and save the plot as an image
    data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'])
    anomalies['TIMESTAMP'] = pd.to_datetime(anomalies['TIMESTAMP'], errors='coerce')  # Suppress warning here

    plt.figure(figsize=(12, 6))
    plt.plot(data['TIMESTAMP'], data['total_failures'], label='Total Failures', color='blue', marker='o')
    plt.scatter(anomalies['TIMESTAMP'], anomalies['total_failures'], color='red', label='Anomaly', marker='x')
    plt.xlabel('Timestamp')
    plt.ylabel('Total Failures')
    plt.title('Anomaly Detection in Prowler Scan Results')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    #plt.show()

    # Save the plot to a file in the Anomaly_test folder
    plot_path = output_dir / "anomaly_detection_plot.png"

    # Delete the previous plot if it exists
    if plot_path.exists():
        plot_path.unlink()

    plt.savefig(plot_path)
    plt.close()  # Close the plot to prevent it from showing in the terminal

    # Send anomalies and plot to Slack
    upload_success = send_anomaly_report_to_slack(anomalies, plot_path)

    # Delete the plot after sending to Slack if the upload was successful
    if upload_success and plot_path.exists():
        plot_path.unlink()

if __name__ == "__main__":
    main()