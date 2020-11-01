from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, render_template, request
import key_config as keys
import boto3
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

app = Flask(__name__)

ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID")
ACCESS_SECRET_KEY = os.environ.get("ACCESS_SECRET_KEY")
DYNAMODB_NAME = os.environ.get("DYNAMODB_NAME")

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=ACCESS_KEY_ID,
                          aws_secret_access_key=ACCESS_SECRET_KEY
                          )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['post'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        table = dynamodb.Table(DYNAMODB_NAME)

        table.put_item(
            Item={
                'name': name,
                'email': email,
                'password': password
            }
        )
        msg = "Registration Complete. Please Login to your account !"

        return render_template('login.html', msg=msg)
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/check', methods=['post'])
def check():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        table = dynamodb.Table(DYNAMODB_NAME)
        response = table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        name = items[0]['name']
        print(items[0]['password'])
        if password == items[0]['password']:

            return render_template("home.html", name=name)
    return render_template("login.html")


@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == "__main__":

    app.run(debug=True)
