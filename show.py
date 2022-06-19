import json
import boto3
from botocore.exceptions import ClientError
import config
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

def handler(event, context):
    try:
        config.create_table()
        return show_item(event['pathParameters']['id'])
    except ClientError as e:
        print(e)
        return {'statusCode': 500, 'body':  json.dumps({'error': e.response['Error']['Message']})}


def show_item(id):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('People')
    response = table.query(
        KeyConditionExpression=Key('id').eq(id)
    )
    items = response['Items']
    return {
        'statusCode': 200,
        'body': json.dumps(items, cls=DecimalEncoder)

    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
