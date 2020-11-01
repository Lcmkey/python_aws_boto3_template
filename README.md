# DynamoDB - How to run

1. Create .env in project root directory as below content

   ```properties
    ACCESS_KEY_ID=
    ACCESS_SECRET_KEY=

    # DynamoDB
    DYNAMODB_USERS_TABLE=users-demo-sam
    DYNAMODB_BOOKS_TABLE=books-demo-sam
    DYNAMODB_EMPLOYEES_TABLE=employees-demo-sam
    DYNAMODB_POSTS_TABLE=posts-demo-sam

    # Rds
    RDS_ENDPOINT=
    DB_IDENTIFIER=rds_demo_sam
    RDS_DN_PORT=3306
    RDS_DB_USER=
    RDS_DB_PASSWORD=
    RDS_DB_NAME=rds_demo_sam
    RDS_SG_ID=

    # S3
    S3_BUCKET_NAME=boto3-bucket-demo-sam

   ```

2. Create DynamoDB Table

   ```properties
   $ python3 ./DynamoDB/dynamoDB_create_table.py create_hashKey_table
   ```

   Event Actions:

   - create_hashKey_table
   - create_hashKey_and_range_table
   - create_gsi_table
   - create_lsi_table

3. Execute User Event

   ```properties
   $ python3 ./DynamoDB/dynamoDB_events.py create_user get_user update_user get_user
   ```

   Event Action:

   - create_user
   - get_user
   - query_user
   - update_user
   - delete_user
   - create_batch_user
   - scan_first_last_user
   - scan_multi_user
   - create_books
   - fetch_range_data_books
   - create_employee
   - query_emp_data_gsi
   - create_posts
   - query_post_data_lsi

# RDS - How to run

1. Create .env in project root directory as DynamoDB Stes 1

2. Create Mysql Instance

   ```properties
   $ python3 ./RDS/rds_create_instance.py
   ```

3. Test Events

   ```properties
   $ python3 ./RDS/rds_db_events.py create_table insert_details get_details
   ```

   Event Action:

   - create_table
   - insert_details
   - get_details

# S3 - How to run

1. Create .env in project root directory as DynamoDB Stes 1

2. Create S3 Bucket
  ```properties
  $ python3 ./S3/S3_bucket.py create_bucket
  ```
2. Run Application

   ```properties
   $ python3 app_s3.py
   ```

3. Browse http://127.0.0.1:5000/ && upload your file
