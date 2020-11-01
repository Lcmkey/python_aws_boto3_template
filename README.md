# How to run

1. Create .env in project root directory as below content

    ```properties
    ACCESS_KEY_ID=
    ACCESS_SECRET_KEY=
    DYNAMODB_USERS_TABLE=users-demo-sam
    DYNAMODB_BOOKS_TABLE=books-demo-sam
    DYNAMODB_EMPLOYEES_TABLE=employees-demo-sam
    DYNAMODB_POSTS_TABLE=posts-demo-sam
    ```

2. Create DynamoDB Table

    ```properties
    $ python3 dynamoDB_create_table.py create_hashKey_table
    ```

    Event Actions:
    - create_hashKey_table
    - create_hashKey_and_range_table
    - create_gsi_table
    - create_lsi_table

3. Execute User Event 

    ```properties
    $ python3 dynamoDB_events.py create_user get_user update_user get_user
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