import json
import boto3
from botocore.exceptions import ClientError
import config
import show
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr


def handler(event, context):
    try:
        config.create_table()
        return delete(event['pathParameters']['id'])
    except ClientError as e:
        print(e)
        return {'statusCode': 500, 'body':  json.dumps({'error': e.response['Error']['Message']})}


def delete(id):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('People')
    item = json.dumps(show.show_item(id))
    data = json.loads(item)
    body = json.loads(data['body'])
    res = table.delete_item(
        Key={
            'id': id,
            'createdAt': int(body[0]['createdAt'])
        }
    )
    return {
        'statusCode': 200,
        'body':  json.dumps({'message': 'success'})
    }
