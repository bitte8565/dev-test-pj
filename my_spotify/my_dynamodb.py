import os

import boto3

env = os.getenv('env', 'local')
if env == 'local':
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000",
                              region_name='us-west-2',
                              aws_access_key_id='ACCESS_ID',
                              aws_secret_access_key='ACCESS_KEY')
else:
    dynamodb = boto3.resource('dynamodb')


def delete_table(table_name):
    table = dynamodb.Table(table_name)
    table.delete()


def put_item(table, item):
    table = dynamodb.Table(table)
    table.put_item(
        Item=item
    )


def get_item(table, artist):
    table = dynamodb.Table(table)
    response = table.get_item(Key=artist)
    return response['Item']


def create_spotify_followed_artist_latest_album(table_name):
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'artist_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'artist_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print('Table status:', table.table_status)


def get_all_item(table_name):
    table = dynamodb.Table(table_name)
    response = table.scan()
    return response['Items']


def init_table():
    table_name = 'spotify_followed_artist_latest_album'
    delete_table(table_name)
    create_spotify_followed_artist_latest_album('spotify_followed_artist_latest_album')
    artist = {'artist_id': 'aaaa'}
    album = {'album_id': 'bbb'}
    item = dict(**artist, **album)
    put_item(table_name, item)
    item = get_item(table_name, artist)


if __name__ == '__main__':
    init_table()

