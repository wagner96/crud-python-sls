import json
import boto3
from botocore.exceptions import ClientError
import show
import config


def handler(event, context):
    body = json.loads(event['body'])
    id = event['pathParameters']['id']
    try:
        config.create_table()
        return update(body['name'], body['email'], id)
    except ClientError as e:
        print(e)
        return {'statusCode': 500, 'body':  json.dumps({'error': e.response['Error']['Message']})}

def update(name, email, id):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('People')
    item = json.dumps(show.show_item(id))
    data = json.loads(item)
    body = json.loads(data['body'])
    table.update_item(
        Key={
            'id': id,
            'createdAt': int(body[0]['createdAt'])
        },
        UpdateExpression="SET #nam=:n, email=:e",
        ExpressionAttributeValues={
            ':n': name,
            ':e': email
        },
        ExpressionAttributeNames={
            "#nam": "name"
        },
        ReturnValues="UPDATED_NEW"
    )
    return {
        'statusCode': 200,
        'body': json.dumps({'name': name,
                            'email': email
                            })
    }
