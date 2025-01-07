# <b>Cloud Security Analysis and Automation using AI/ML</b>

## Project Description
An automated cloud security analysis tool that integrates Prowler security checks with machine learning for anomaly detection and risk prediction in AWS environments.

## Prerequisites
- Python 3.8 or higher
- AWS CLI configured with appropriate credentials
- Required Python packages (listed in `requirements.txt`)

## AWS CLI Configuration

1. **Install AWS CLI**:
   ```bash
   sudo apt-get update;
   sudo apt-get install awscli

2. **Verify AWS CLI installation**:
   ```bash
   aws --version

3. **Configure AWS Credentials**:
   ```bash
   aws configure

4. **You will be prompted for**:


- AWS Access Key ID
- AWS Secret Access Key
- Default region name (e.g., us-east-1)
- Default output format (json)
  
5. **Verify configuration**:
   ```bash
   aws sts get-caller-identity

6. **Expected output**:
   ```bash
  {
      "UserId": "USERID",
      "Account": "123456789012",
      "Arn": "arn:aws:iam::123456789012:user/YourUsername"
  }

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/madan03/Cloud_SecAI.git
   cd Cloud_SecAI

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt

3. **Configure environment variables: Create a .env file with**:
   ```bash
   SLACK_WEBHOOK_URL=your_webhook_url
   SLACK_API_TOKEN=your_api_token

## Usage
1. **Run the complete analysis pipeline**:
   ```bash
   python3 app.py



## This will execute:
1. Prowler installation check
2. Security scan using Prowler
3. Data preprocessing
4. Anomaly detection
5. Machine learning analysis

## Features:
- Automated AWS security scanning using Prowler
- Data preprocessing and aggregation
- Anomaly detection using Isolation Forest
- Risk prediction using Random Forest
- Slack integration for notifications
- Automated report generation

## Configuration:
- Modify scan parameters in `run_prowler.py`
- Adjust anomaly detection settings in `anomaly.py`
- Configure ML parameters in `Pre_anal_ml.py`








    


