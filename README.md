# <b>Cloud Security Analysis and Automation using AI/ML</b>

## Project Description
An automated cloud security analysis tool that integrates Prowler security checks with machine learning for anomaly detection and risk prediction in AWS environments.

## Prerequisites
- Python 3.10 or higher
- AWS CLI configured with appropriate credentials
- Required Python packages (listed in `requirements.txt`)

## Setting up a Python Virtual Environment
1. **Install Python (if not already installed)**:
Ensure that Python 3.8 or higher is installed. You can verify your Python version with the following command:
    ```bash
    python3 --version
2. **Create a Virtual Environment**:
    ```bash
    python3 -m venv abcenv
3. **Activate the Virtual Environment**:
3.1 **For Linux/macOS**:
    ```bash
    source abcenv/bin/activate 

3.2 **For Windows**:
    
    .\abcenv\Scripts\activate


## AWS CLI Configuration

1. **Install AWS CLI**:
   ```bash
   sudo apt-get update
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
   SLACK_CHANNEL_ID=your_slack_channel_id

## Usage
1. **Run the complete analysis pipeline**:
   ```bash
   python3 app.py

## Docker Support

1. **Building the container**:
    ```bash
    docker build -t cloud-sec-ai .

## Running with Docker 
1. **Create .env file with your credentials**:
   ```bash
   SLACK_WEBHOOK_URL=your_webhook_url
   SLACK_API_TOKEN=your_api_token
   AWS_ACCESS_KEY_ID=your_aws_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret
   AWS_DEFAULT_REGION=your_aws_region

2. **Run the container**:
   ```bash
   docker run --env-file .env cloud-sec-ai

## Docker Compose Support of this project::
1. **Run the Docker compose file**:
   ```bash
   docker compose -f dockerfile up -d

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

## Special Thanks

**Special thanks to**:
- [Prowler](https://github.com/prowler-cloud/prowler) - The open-source security tool for AWS that made this project possible
- The entire Prowler community for their contributions and support
- AWS Security community for their continuous guidance









    


