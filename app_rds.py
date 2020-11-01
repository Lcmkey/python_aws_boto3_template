import sys
import RDS.rds_db_events as db
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
from flask import Response, send_file

app = Flask(__name__, template_folder="./RDS/templates")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/insert', methods=['post'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        gender = request.form['optradio']
        comment = request.form['comment']
        db.insert_details(name, email, comment, gender)
        details = db.get_details()

        print(details)

        for detail in details:
            var = detail
        return render_template('index.html', var=var)


if __name__ == "__main__":
    app.run(debug=True)
