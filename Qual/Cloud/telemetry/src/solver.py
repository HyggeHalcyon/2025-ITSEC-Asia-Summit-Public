import boto3
import datetime
import time

aws_access_key_id = "XXX"
aws_secret_access_key = "XXX"

s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

bucket_name = "prompter-d4a788638b06b9813ce51a45aee69430"

while True:
    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        timestamp = now.strftime('%Y%m%dT%H%M') + 'Z'
        key = f'prometheus-export/metrics-{timestamp}.prom'
        
        print(f"Trying to access: s3://{bucket_name}/{key}")
        response = s3.get_object(Bucket=bucket_name, Key=key)
        print(response['Body'].read().decode('utf-8'))
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)
