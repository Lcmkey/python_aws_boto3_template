import os
import sys
import pymysql
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

RDS_ENDPOINT = os.environ.get("RDS_ENDPOINT")
RDS_DN_PORT = os.environ.get("RDS_DN_PORT")
RDS_DB_USER = os.environ.get("RDS_DB_USER")
RDS_DB_PASSWORD = os.environ.get("RDS_DB_PASSWORD")
RDS_DB_NAME = os.environ.get("RDS_DB_NAME")


conn = pymysql.connect(
    host=RDS_ENDPOINT,  # endpoint link
    port=int(RDS_DN_PORT),  # 3306
    user=RDS_DB_USER,
    password=RDS_DB_PASSWORD,
    db=RDS_DB_NAME,

)

"""
Table Creation
"""


def create_table():
    cursor = conn.cursor()
    create_table = """
    create table Details (name varchar(200),email varchar(200),comment varchar(200),gender varchar(20) )
    """

    cursor.execute(create_table)


"""
Insert Data
"""


def insert_details(name, email, comment, gender):
    cur = conn.cursor()
    cur.execute("INSERT INTO Details (name,email,comment,gender) VALUES (%s,%s,%s,%s)",
                (name, email, comment, gender)
                )

    conn.commit()


"""
Get Data
"""


def get_details():
    cur = conn.cursor()
    cur.execute("SELECT *  FROM Details")
    details = cur.fetchall()
    print(details)
    return details


def user_action(event):
    return {
        "create_table": create_table,
        "insert_details": insert_details,
        "get_details": get_details,
    }[event]


print("Number of arguments: %i %s" % (len(sys.argv), "arguments."))
print("Argument List: %s" % str(sys.argv))

args = sys.argv
del args[0]

for current_argument in args:
    action = current_argument
    if action == "insert_details":
        result = user_action(action)(
            "Sam Leung", "lcm@samleung.me", "Hello World", "M")
    else:
        result = user_action(action)()
