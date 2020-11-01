import os
import sys
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        print(e)
        return False
    return True


# Retrieve the list of existing buckets
def list_buckets():
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()

    # Output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')


def user_action(event):
    return {
        "create_bucket": create_bucket,
        "list_bucket": list_buckets,
    }[event]


print("Number of arguments: %i %s" % (len(sys.argv), "arguments."))
print("Argument List: %s" % str(sys.argv))

args = sys.argv
del args[0]

for current_argument in args:
    action = current_argument
    if action == "create_bucket":
        result = user_action(action)(S3_BUCKET_NAME)
    else:
        result = user_action(action)()
