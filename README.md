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
  AWS Access Key ID
  AWS Secret Access Key
  Default region name (e.g., us-east-1)
  Default output format (json)

5. **Verify configuration**:
   ```bash
   aws sts get-caller-identity

**Expected output**:
``bash
{
  "UserId": "USERID",
  "Account": "123456789012",
  "Arn": "arn:aws:iam::123456789012:user/YourUsername"
}



    


