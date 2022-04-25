import pandas
import boto3
import asyncio

# it can change value for your custom dataset
SOURCE_CSV_FILE="tcc_ceds_music.csv"
DYNAMODB_TABLE_NAME="Musics"

async def main():
    # will store coroutines to this variable
    coroutines = list()
    # boto3 client connections
    client = [ boto3.client('dynamodb') for n in range(1,11) ]
    with open(SOURCE_CSV_FILE, newline='') as file:
        reader = pandas.read_csv(file, chunksize=25)
        n = 0 # client connection number
        for df in reader:
            # data frame parse and transform to dynamodb batch_write_item request format
            requests = df_transform_to_dynamodb_batch_write_items_put(df)
            # dynamodb batch_write_item api call
            coroutines.append( dynamodb_batch_write_item(requests, client[n]))
            # client connection number
            n = n+1 if n < 9 else 0
    # wait for result async coroutines
    await asyncio.gather(*coroutines)

def df_transform_to_dynamodb_batch_write_items_put(df: pandas.DataFrame) -> list:
    # data frame parse and transform to dynamodb batch_write_item request format
    return [
        {
            "PutRequest": {
                "Item": {
                    col: (
                        {"N": str(row)} if type(row) in [float,int] else
                        {"S": row}
                    )
                    for col, row in csv_item.items()
                }
            }
        }
        for csv_item in df.to_dict('records')
    ]

def df_transform_to_dynamodb_batch_write_items_delete(df: pandas.DataFrame) -> list:
    # data frame parse and transform to dynamodb batch_write_item request format
    return [
        {
            "DeleteRequest": {
                "Key": {
                    col: (
                        {"N": str(row)} if type(row) in [float,int] else
                        {"S": row}
                    )
                    for col, row in csv_item.items()
                    if col in ['artist_name','track_name']
                }
            }
        }
        for csv_item in df.to_dict('records')
    ]

async def dynamodb_batch_write_item(requests, client):
    try:
        response = client.batch_write_item(
            RequestItems={
                DYNAMODB_TABLE_NAME: requests
            },
            ReturnConsumedCapacity='TOTAL',
            ReturnItemCollectionMetrics='SIZE'
        )
    except Exception as error:
        print(error)
        exit(1)

if __name__ == "__main__":
    print(f"SOURCE_CSV_FILE: {SOURCE_CSV_FILE}")
    print(f"DYNAMODB_TABLE_NAME: {DYNAMODB_TABLE_NAME}")
    while True:
        confirm = input("Are you sure you want create dynamodb table and items (y/n)? ")
        if confirm == 'y':
            asyncio.run(main())
            print("Done!")
            exit(0)
        elif confirm == 'n':
            print("Cancled")
            exit(1)
        else:
            print("Only input 'y' or 'n', Try again! ")