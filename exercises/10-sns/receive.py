import boto3

client = boto3.client('sqs')
response = client.receive_message(QueueUrl = 'https://sqs.us-east-1.amazonaws.com/911739205087/api-payments')

print(response)
