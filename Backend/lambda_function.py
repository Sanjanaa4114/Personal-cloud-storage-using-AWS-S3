import boto3
import json
import os
import uuid
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FileMetadata')
BUCKET_NAME = 'my-cloud-storage-username'

def lambda_handler(event, context):
    action = event.get('action')
    
    if action == 'upload':
        file_name = event['file_name']
        user = event['user']
        file_id = str(uuid.uuid4())
        
        s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=event['file_content'])
        
        table.put_item(Item={
            'fileId': file_id,
            'fileName': file_name,
            'user': user,
            'uploadTime': datetime.utcnow().isoformat()
        })
        return {'message': 'File uploaded successfully'}

    elif action == 'list':
        user = event['user']
        response = table.scan()
        return {'files': response['Items']}

    elif action == 'delete':
        file_name = event['file_name']
        s3.delete_object(Bucket=BUCKET_NAME, Key=file_name)
        return {'message': 'File deleted successfully'}

    else:
        return {'error': 'Invalid action'}
