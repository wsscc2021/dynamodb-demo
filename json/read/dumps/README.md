
It make dump items for practices about read operations.

# Quick Start

1. Create DynamoDB table
    - Table Name : *Musics*
    - Partition Key : *artist_name*
    - Sort Key : *track_name*
    - On-demand

2. Download source
    ```
    git clone https://github.com/wsscc2021/dynamodb-demo
    ```

3. (Optional) Change constant in script for your custom dataset.
    `json/read/dumps/put_dump_items.py`
    ```
    # it can change value for your custom dataset
    SOURCE_CSV_FILE="tcc_ceds_music.csv"
    DYNAMODB_TABLE_NAME="Musics"
    ```

3. Create virtual environment and install python packages
    ```
    cd dynamodb-demo/json/read/dumps/
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
    ```

4. Setting your aws credential and config
    - please ref for aws docs
        - [configure by credential files](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) 
        - [configure by environment](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)

    - verify credential
        ```
        aws sts get-caller-identity
        ```
    - verify configured region
        ```
        aws configure get region
        ```

5. Run Script
    ```
    python3 put_dump_items.py
    ```

6. Continue practices about read operations.

7. Delete DynamoDB table that used at practices.