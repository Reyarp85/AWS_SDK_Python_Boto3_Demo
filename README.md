##  AWS SDK Python Boto3 Demos

This repository contains demos using AWS SDK Python Boto3 to interact with different AWS services.
- [Demo01-Sentiment Analysis](./Demo01-SentimentAnalysis)
- [Demo02-Finding Unused Security Groups](./Demo02-FindingUnusedSecurityGroups)
- [Demo03-Image Rekognition Web App](./Demo03-ImageRekognitionWebApp)

## Requirements
- Python 3.8 or later (Download and install via https://www.python.org/downloads/)
- An AWS account (Sign up via https://aws.amazon.com/account/sign-up)
  - IAM user with access keys

## Setting up
1. (Optional) Create a Virtual Environment
```python
python -m venv venv
```
Activate the virtual environment:
- On Windows:
```shell
.\venv\Scripts\activate
```
- On macOS or Linux:
```shell
source venv/bin/activate 
```
2. Install Dependencies
```shell
pip install -r requirements.txt
```