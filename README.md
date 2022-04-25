
## Read Operations
0. Prepare dumps for practices read operations. please refer to `json/read/dumps`

1. get-item
    ```
    aws dynamodb get-item --table-name Musics --key file://json/read/get_item.json
    ```

2. scan
    - use scan-filter
        ```
        aws dynamodb scan --table-name Musics \
            --return-consumed-capacity TOTAL \
            --scan-filter '{
                "artist_name": {
                    "AttributeValueList": [ {"S": "bts"} ],
                    "ComparisonOperator": "EQ"
                }
            }'
        ```
    - use expression
        ```
        aws dynamodb scan --table-name Musics \
            --return-consumed-capacity TOTAL \
            --filter-expression 'artist_name = :artist' \
            --expression-attribute-values '{
                ":artist": {"S": "bts"}
            }'
        ```
    - response (it performed full-scanned)
        ```
        {
            ...
            "Count": 6,
            "ScannedCount": 28372,
            "ConsumedCapacity": {
                "TableName": "Musics",
                "CapacityUnits": 128.5
            }
        }
        ```

3. query
    - use query-filter
        ```
        aws dynamodb query --table-name Musics \
            --return-consumed-capacity TOTAL \
            --key-conditions '{
                "artist_name": {
                    "ComparisonOperator": "EQ",
                    "AttributeValueList": [ {"S": "bts"} ]
                }
            }'
        ```
    - use expression
        ```
        aws dynamodb query --table-name Musics \
            --return-consumed-capacity TOTAL \
            --key-condition-expression 'artist_name = :artist' \
            --expression-attribute-values '{
                ":artist": {"S": "bts"}
            }'
        ```
    - response (it scanned only partitioned dataset)
        ```
        {
            ...
            "Count": 6,
            "ScannedCount": 6,
            "ConsumedCapacity": {
                "TableName": "Musics",
                "CapacityUnits": 1.0
            }
        }
        ```

## Write Operations

1. put-item
    ```
    aws dynamodb put-item --table-name AlbumList --item file://json/write/put_item.json
    ```

2. delete-item
    ```
    aws dynamodb delete-item --table-name --key file://json/write/delete_item.json
    ```

3. batch-write-item
    ```
    aws dynamodb batch-write-item --request-items file://json/write/batch_write_item_put.json
    ```
    ```
    aws dynamodb batch-write-item --request-items file://json/write/batch_write_item_delete.json
    ```