import boto3


def create_table():
    client = boto3.client('dynamodb')
    tables = client.list_tables()
    if 'People' in tables['TableNames']:
        table_found = True
    else:
        table_found = False
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.create_table(
            TableName='People',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'createdAt',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'createdAt',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
    return table_found
