import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
import boto3
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
app = Flask(__name__, template_folder="./S3/templates")

ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID")
ACCESS_SECRET_KEY = os.environ.get("ACCESS_SECRET_KEY")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

s3 = boto3.client('s3',
                  aws_access_key_id=ACCESS_KEY_ID,
                  aws_secret_access_key=ACCESS_SECRET_KEY,
                  )


@app.route('/')
def home():
    return render_template("file_upload.html")


@app.route('/upload', methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
            filename = secure_filename(img.filename)
            img.save("./upload/" + filename)
            s3.upload_file(
                Bucket=S3_BUCKET_NAME,
                Filename="./upload/" + filename,
                Key=filename
            )
            msg = "Upload Done ! "

    return render_template("file_upload.html", msg=msg)


if __name__ == "__main__":

    app.run(debug=True)
