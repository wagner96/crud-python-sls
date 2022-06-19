import json
import boto3
from botocore.exceptions import ClientError
import config
from datetime import datetime
import uuid


def handler(event, context):
    body = json.loads(event['body'])
    try:
        config.create_table()
        return create(body['name'], body['email'])
    except ClientError as e:
        print(e)
        return {'statusCode': 500, 'body':  json.dumps({'error': e.response['Error']['Message']})}


def create(name, email):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('People')
    dt = datetime.now()
    table.put_item(
        Item={
            'id': uuid.uuid4().hex,
            'createdAt': int(datetime.timestamp(dt)),
            'name': name,
            'email': email
        }

    )
    return {
        'statusCode': 200,
        'body': json.dumps({'name': name,
                            'email': email
                            })
    }
