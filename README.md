##### Cloud_SecAI #####
<h1><b>Cloud Security Analysis and Automation using AI/ML</b></h1>

## Project Description
An automated cloud security analysis tool that integrates Prowler security checks with machine learning for anomaly detection and risk prediction in AWS environments.

## Prerequisites
- Python 3.8 or higher
- AWS CLI configured with appropriate credentials
- Prowler
- Required Python packages (listed in requirements.txt)


## Installation
1. Clone the repository:
cmd: bash
git clone https://github.com/madan03/Cloud_SecAI.git
cd Cloud_SecAI


2.Install required packages:
pip install -r requirements.txt

3.Configure environment variables: Create a .env file with:
SLACK_WEBHOOK_URL=your_webhook_url
SLACK_API_TOKEN=your_api_token

Usage
Run the complete analysis pipeline:
python3 app.py


**This will execute:
1.Prowler installation check
2.Security scan using Prowler
3.Data preprocessing
4.Anomaly detection
5.Machine learning analysis

**Features::
**
 ->Automated AWS security scanning using Prowler
->Data preprocessing and aggregation
->Anomaly detection using Isolation Forest
->Risk prediction using Random Forest
->Slack integration for notifications
->Automated report generation

**Configuration::
**
Modify scan parameters in run_prowler.py
Adjust anomaly detection settings in anomaly.py
Configure ML parameters in Pre_anal_ml.py




