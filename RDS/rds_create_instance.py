import time
import os
import boto3
import botocore
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

RDS_DB_USER = os.environ.get("RDS_DB_USER")
RDS_DB_PASSWORD = os.environ.get("RDS_DB_PASSWORD")
RDS_DB_NAME = os.environ.get("RDS_DB_NAME")
RDS_SG_ID = os.environ.get("RDS_SG_ID")


def main():
    db_identifier = 'rds-demo-sam'
    rds = boto3.client('rds')

    try:
        rds.create_db_instance(DBInstanceIdentifier=db_identifier,
                               AllocatedStorage=200,
                               DBName=RDS_DB_NAME,
                               Engine='MySQL',
                               # General purpose SSD
                               StorageType='gp2',
                               StorageEncrypted=False,
                               AutoMinorVersionUpgrade=True,
                               MultiAZ=False,
                               MasterUsername=RDS_DB_USER,
                               MasterUserPassword=RDS_DB_PASSWORD,
                               VpcSecurityGroupIds=[RDS_SG_ID],
                               DBInstanceClass='db.t3.small',
                               Tags=[{'Key': 'MyTag', 'Value': 'TagValue'}])
        print('Starting RDS instance with ID: %s' % db_identifier)
    except botocore.exceptions.ClientError as e:
        # if 'DBInstanceAlreadyExists' in e.response.message:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print('DB instance %s exists already, continuing to poll ...' %
                  db_identifier)
        else:
            raise

    running = True
    while running:
        response = rds.describe_db_instances(
            DBInstanceIdentifier=db_identifier)

        db_instances = response['DBInstances']
        if len(db_instances) != 1:
            raise Exception(
                'Whoa cowboy! More than one DB instance returned; this should never happen')

        db_instance = db_instances[0]

        status = db_instance['DBInstanceStatus']

        print('Last DB status: %s' % status)

        time.sleep(5)
        if status == 'available':
            endpoint = db_instance['Endpoint']
            host = endpoint['Address']
            # port = endpoint['Port']

            print('DB instance ready with host: %s' % host)
            running = False


if __name__ == '__main__':
    main()
