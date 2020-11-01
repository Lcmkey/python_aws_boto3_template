import sys
import boto3
from boto3.dynamodb.conditions import Key
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID")
ACCESS_SECRET_KEY = os.environ.get("ACCESS_SECRET_KEY")
DYNAMODB_USERS_TABLE = os.environ.get("DYNAMODB_USERS_TABLE")
DYNAMODB_BOOKS_TABLE = os.environ.get("DYNAMODB_BOOKS_TABLE")
DYNAMODB_EMPLOYEES_TABLE = os.environ.get("DYNAMODB_EMPLOYEES_TABLE")
DYNAMODB_POSTS_TABLE = os.environ.get("DYNAMODB_POSTS_TABLE")

dynamodb = boto3.resource("dynamodb",
                          aws_access_key_id=ACCESS_KEY_ID,
                          aws_secret_access_key=ACCESS_SECRET_KEY
                          )


def create_user():
    user = {
        "email": "lcm@samleung.me",
        "preferred_name": "Sam Leung",
        "firt_name": "Sam",
        "last_name": "Leung",
        "password": "your-password"
    }

    table = dynamodb.Table(DYNAMODB_USERS_TABLE)

    table.put_item(Item=user)


def get_item():
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(DYNAMODB_USERS_TABLE)

    resp = table.get_item(
        Key={
            "email": "lcm@samleung.me",
        }
    )

    if "Item" in resp:
        print(resp["Item"])


def query():
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(DYNAMODB_USERS_TABLE)

    resp = table.query(
        KeyConditionExpression=Key("email").eq("lcm@samleung.me")
    )

    if "Items" in resp:
        print(resp["Items"][0])


def update():
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(DYNAMODB_USERS_TABLE)

    table.update_item(
        Key={
            "email": "lcm@samleung.me",
        },
        UpdateExpression="set preferred_name = :g",
        ExpressionAttributeValues={
            ":g": "Sam Leung - Update"
        },
        ReturnValues="UPDATED_NEW"
    )

    get_item()


def delete_user():
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(DYNAMODB_USERS_TABLE)

    table.delete_item(
        Key={
            "email": "lcm@samleung.me",
        },
    )


"""
Using the same table from the above, let"s go ahead and create a bunch of users.
"""


def create_bunch_of_users():
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(DYNAMODB_USERS_TABLE)

    for n in range(3):
        table.put_item(
            Item={
                "email": "sam.leung" + str(n) + "@masterson-tech.com",
                "preferred_name": "Sam" + str(n) + " Leung",
                "first_name": "Sam" + str(n),
                "last_name": "Leung",
                "password": "your-password"
            }
        )


"""
We can see above that all the attributes are being returned.

Here is an example of just scanning for all first & last names in the database:
"""


def scan_first_and_last_names():
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(DYNAMODB_USERS_TABLE)

    resp = table.scan(ProjectionExpression="first_name, last_name")

    print(resp["Items"])


"""
Scans have a 1mb limit on the data returned.
If we think we’re going to exceed that,
we should continue to re-scan and pass in the LastEvaluatedKey:
"""


def multi_part_scan():
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(DYNAMODB_USERS_TABLE)

    response = table.scan()
    result = response["Items"]

    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        result.extend(response["Items"])

    print(result)


def create_books():
    book = {
        "title": "This is a Good Book",
        "author": "Sam Leung",
        "year": "1980"
    }

    another_book = {
        "title": "This is a Good Book",
        "author": "Hello World",
        "year": "1998"
    }

    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(DYNAMODB_BOOKS_TABLE)

    table.put_item(Item=book)
    table.put_item(Item=another_book)


def fetch_data_with_range():
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(DYNAMODB_BOOKS_TABLE)

    resp = table.get_item(
        Key={
            "title": "This is a Good Book",
            "author": "Sam Leung"
        }
    )

    print(resp["Item"])
    #{"year": "1998", "title": "This is a Good Book", "author": "Sam Leung"}

    resp = table.query(
        KeyConditionExpression=Key("title").eq(
            "This is a Good Book") & Key("author").eq("Sam Leung")
    )

    print(resp["Items"][0])


def create_employee():
    user = {
        "emp_id": 1,
        "first_name": "Sam",
        "last_name": "Leung",
        "email": "lcm@samleung.me"
    }

    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(DYNAMODB_EMPLOYEES_TABLE)

    table.put_item(Item=user)


"""
At the time of writing this get_item on GSI is not supported.
"""


def query_data_with_gsi():
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(DYNAMODB_EMPLOYEES_TABLE)

    response = table.query(
        IndexName="email",
        KeyConditionExpression=Key("email").eq("lcm@samleung.me")
    )

    if len(response["Items"]) > 0:
        print(response["Items"][0])
    else:
        print("No match data")


def create_posts():
    post1 = {
        "title": "My favorite hiking spots",
        "user_name": "sam.leung",
        "subject": "hiking"
    }

    post2 = {
        "title": "My favorite recipes",
        "user_name": "sam.leung",
        "subject": "cooking"
    }

    post3 = {
        "title": "I love hiking!",
        "user_name": "hello_world",
        "subject": "hiking"
    }

    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(DYNAMODB_POSTS_TABLE)

    table.put_item(Item=post1)
    table.put_item(Item=post2)
    table.put_item(Item=post3)


"""
At the time of writing this get_item on GSI is not supported.
"""


def query_data_with_lsi():
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table(DYNAMODB_POSTS_TABLE)

    response = table.query(
        IndexName="user_name_subject",
        KeyConditionExpression=Key("user_name").eq(
            "sam.leung") & Key("subject").eq("hiking")
    )
    if len(response["Items"][0]) > 0:
        print(response["Items"][0])
    else:
        print("No match data")


"""
User arguments action
"""


def user_action(event):
    print(event)
    return {
        # "create": lambda event: create_user(),
        # "get": lambda event: get_item(),
        "create_user": create_user,
        "get_user": get_item,
        "query_user": query,
        "update_user": update,
        "delete_user": delete_user,
        "create_batch_user": create_bunch_of_users,
        "scan_first_last_user": scan_first_and_last_names,
        "scan_multi_user": multi_part_scan,
        "create_books": create_books,
        "fetch_range_data_books": fetch_data_with_range,
        "create_employee": create_employee,
        "query_emp_data_gsi": query_data_with_gsi,
        "create_posts": create_posts,
        "query_post_data_lsi": query_data_with_lsi
    }[event]


print("Number of arguments: %i %s" % (len(sys.argv), "arguments."))
print("Argument List: %s" % str(sys.argv))

args = sys.argv
del args[0]

for current_argument in args:
    action = current_argument
    result = user_action(action)()
    # result("create")  # lambda
