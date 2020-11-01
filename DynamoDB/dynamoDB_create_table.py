import sys
import boto3
import os
# from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
# from pathlib import Path  # Python 3.6+ only
# import key_config as keys

# load_dotenv()
load_dotenv(find_dotenv())
# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

# OR, the same with increased verbosity
# load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)

ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID")
ACCESS_SECRET_KEY = os.environ.get("ACCESS_SECRET_KEY")
DYNAMODB_USERS_TABLE = os.environ.get("DYNAMODB_USERS_TABLE")
DYNAMODB_BOOKS_TABLE = os.environ.get("DYNAMODB_BOOKS_TABLE")
DYNAMODB_EMPLOYEES_TABLE = os.environ.get("DYNAMODB_EMPLOYEES_TABLE")
DYNAMODB_POSTS_TABLE = os.environ.get("DYNAMODB_POSTS_TABLE")

dynamodb = boto3.resource('dynamodb',
                          #   aws_access_key_id=keys.ACCESS_KEY_ID,
                          #   aws_secret_access_key=keys.ACCESS_SECRET_KEY
                          aws_access_key_id=ACCESS_KEY_ID,
                          aws_secret_access_key=ACCESS_SECRET_KEY
                          )

# # dynamodb = boto3.resource('dynamodb')

"""
STRING = "S"
NUMBER = "N"
BINARY = "B"
STRING_SET = "SS"
NUMBER_SET = "NS"
BINARY_SET = "BS"
NULL = "NULL"
BOOLEAN = "BOOL"
MAP = "M"
LIST = "L"
"""


# Creat a table with just a hash key:
def create_hashKey_table():
    table = dynamodb.create_table(
        TableName=DYNAMODB_USERS_TABLE,
        KeySchema=[
            {
                "AttributeName": "email",
                "KeyType": "HASH"  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "email",
                "AttributeType": "S"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter("table_exists").wait(
        TableName=DYNAMODB_USERS_TABLE)

    # Print out some data about the table.
    print(table.item_count)
    print("Table status:", table.table_status)


"""
Hash + Range Key

Hash and Range Primary Key — The primary key is made of two attributes.
The first attribute is the hash attribute and
the second attribute is the range attribute.
For example, the forum Thread table can have ForumName and
Subject as its primary key,
where ForumName is the hash attribute and Subject is the range attribute.
DynamoDB builds an unordered hash index on the hash attribute and
a sorted range index on the range attribute.

To Demonstrate this next part, we’ll build a table for books.
The title will be our hash key and author will be our range key.
"""


def create_table_with_range():
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName=DYNAMODB_BOOKS_TABLE,
        KeySchema=[
            {
                'AttributeName': 'title',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'author',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'author',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1,
        }
    )

    print("Table status:", table.table_status)


"""
Global Secondary Index (GSI)
Some applications might need to perform many kinds of queries,
using a variety of different attributes as query criteria.
To support these requirements,
you can create one or more global secondary indexes and
issue Query requests against these indexes in Amazon DynamoDB.

To illustrate this we’re going to create
an Employee table with employee_id as our hash kay and email address as our GSI.
"""


def create_table_with_gsi():
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName=DYNAMODB_EMPLOYEES_TABLE,
        KeySchema=[
            {
                'AttributeName': 'emp_id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'emp_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            },

        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'email',
                'KeySchema': [
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1,
                }
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1,
        }
    )

    print("Table status:", table.table_status)


"""
Local Secondary Index (LSI)

Some applications only need to query data using the base table’s primary key.
However, there might be situations where an alternative sort key would be helpful.
To give your application a choice of sort keys,
you can create one or more local secondary indexes
on an Amazon DynamoDB table and issue Query or Scan requests against these indexes.

To demonstrate this we’re going to create a Posts table with user_name as our hash key,
title as our range key and we’ll have a LSI on user_name & subject.
"""


def create_table_with_lsi():
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName=DYNAMODB_POSTS_TABLE,
        KeySchema=[
            {
                'AttributeName': 'user_name',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'user_name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'subject',
                'AttributeType': 'S'
            },

        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': 'user_name_subject',
                'KeySchema': [
                    {
                        'AttributeName': 'user_name',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'subject',
                        'KeyType': 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1,
        }
    )

    print("Table status:", table.table_status)


"""
User arguments action
"""


def user_action(event):
    print(event)
    return {
        "create_hashKey_table": create_hashKey_table,
        "create_hashKey_and_range_table": create_table_with_range,
        "create_gsi_table": create_table_with_gsi,
        "create_lsi_table": create_table_with_lsi
    }[event]


print("Number of arguments: %i %s" % (len(sys.argv), "arguments."))
print("Argument List: %s" % str(sys.argv))

args = sys.argv

action = args[1]
result = user_action(action)()
