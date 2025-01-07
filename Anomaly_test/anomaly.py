import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve Slack Webhook URL from environment variables
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

# Suppress chained assignment warnings
pd.options.mode.chained_assignment = None

# Load preprocessed data
try:
    data = pd.read_csv("../DataPre/output_pre/prowler_aggregated_severity_counts.csv")
except FileNotFoundError:
    print("The file was not found. Please check the path and try again.")

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
        return  # No anomalies detected to send

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
        return

    # Upload the plot image to Slack
    with open(plot_path, 'rb') as file:
        files = {'file': file}
        payload = {
            "filename": os.path.basename(plot_path),
            "initial_comment": "Here is the anomaly detection graph for Prowler Scan Results.",
            "channels": "#scanresult"  # Replace with your Slack channel name or ID
        }
        response = requests.post(SLACK_WEBHOOK_URL, files=files, data=payload)

        if response.status_code == 200:
            print("Plot image uploaded successfully to Slack.")
        else:
            print(f"Failed to upload plot to Slack: {response.status_code} - {response.text}")

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
plt.show()
# Save the plot to a file
plot_path = "anomaly_detection_plot.png"
plt.savefig(plot_path)
plt.close()  # Close the plot to prevent it from showing in the terminal

# Send anomalies and plot to Slack
send_anomaly_report_to_slack(anomalies, plot_path)

# Optional: Delete the plot after sending to Slack
if os.path.exists(plot_path):
    os.remove(plot_path)
