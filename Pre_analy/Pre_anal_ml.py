import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve Slack Webhook URL from environment variables
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

    # Define base paths
    base_dir = Path(__file__).resolve().parent.parent
    input_file_path = base_dir / 'DataPre/output_pre/prowler_aggregated_severity_counts.csv'

    # Load the Prowler scan data
    data = pd.read_csv(input_file_path)

    # Prepare the data and features for prediction
    data['total_failures'] = data[['Critical', 'High', 'Medium', 'Low']].sum(axis=1)
    failure_threshold = data['total_failures'].median()
    data['next_high_failure'] = (data['total_failures'].shift(-1) > failure_threshold).astype(int)
    data = data.dropna()

    features = data[['total_failures', 'Critical', 'High', 'Medium', 'Low']]
    target = data['next_high_failure']

    # Split data for model training
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Train the RandomForest Classifier
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Make predictions and evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)

    # Function to send consolidated alert to Slack
    def send_consolidated_alert_to_slack(services_info, accuracy, classification_report):
        header = "*Automated Security Alert for All Services* :rotating_light:\n\n"
        table_header = "*Service Name* | *Severity* | *Total Failures* | *Risk Level*\n"
        table_divider = "--- | --- | --- | ---\n"

        table_rows = ""
        for service in services_info:
            table_rows += f"{service['SERVICE_NAME']} | {service['Severity']} | {service['Total Failures']} | {service['Risk Level']}\n"
        
        footer = f"\n*Model Evaluation:*\n" \
                 f"Accuracy: {accuracy:.2f}\n" \
                 f"Classification Report:\n```\n{classification_report}\n```"
        
        message = {
            "text": header + table_header + table_divider + table_rows + footer
        }

        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        if response.status_code == 200:
            print("Consolidated alert sent successfully to Slack.")
        else:
            print(f"Failed to send alert to Slack: {response.status_code} - {response.text}")

    # Automation Response for All Services in a Consolidated Notification
    def automated_response_from_file():
        # Load and prepare data from the prowler_aggregated_severity_counts.csv file
        scan_data = pd.read_csv(input_file_path)
        scan_data['total_failures'] = scan_data[['Critical', 'High', 'Medium', 'Low']].sum(axis=1)
        scan_data['predicted_risk'] = model.predict(scan_data[['total_failures', 'Critical', 'High', 'Medium', 'Low']])
        
        # Collect information for each service in a structured format
        services_info = []
        for idx, row in scan_data.iterrows():
            severity = "Critical" if row['Critical'] > 0 else "High" if row['High'] > 0 else "Medium/Low"
            risk_level = "High" if row['predicted_risk'] == 1 else "Low"
            
            services_info.append({
                "SERVICE_NAME": row['SERVICE_NAME'],
                "Severity": severity,
                "Total Failures": row['total_failures'],
                "Risk Level": risk_level
            })
        
        # Send a single consolidated notification to Slack
        send_consolidated_alert_to_slack(services_info, accuracy, classification_rep)

    # Run the consolidated automated response
    automated_response_from_file()

if __name__ == "__main__":
    main()