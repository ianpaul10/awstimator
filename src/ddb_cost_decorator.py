import functools
# from awstimator import Awstimator
from .awstimator import Awstimator


def measure_ddb_cost(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("DECORATOR --> measure_ddb_cost")

        awstimator = Awstimator()
        write_size = 0
        read_size = 0

        def mock_put_item(TableName, Item, **kwargs):
            print("MOCK PUT ITEM")
            print(TableName)
            print(Item)
            nonlocal write_size
            write_size = awstimator.get_size_in_bytes(Item, is_ddb_item=True)
            return original_put_item(TableName=TableName, Item=Item, **kwargs)

        def mock_get_item(TableName, Key, **kwargs):
            nonlocal read_size
            result = original_get_item(TableName=TableName, Key=Key, **kwargs)
            if "Item" in result:
                read_size = awstimator.get_size_in_bytes(
                    result["Item"], is_ddb_item=True
                )
            return result

        # Patch the DynamoDB client methods
        import boto3

        print("PATCHING")

        original_put_item = boto3.client("dynamodb", region_name="us-west-2").put_item
        original_get_item = boto3.client("dynamodb", region_name="us-west-2").get_item
        boto3.client("dynamodb", region_name="us-west-2").put_item = mock_put_item
        boto3.client("dynamodb", region_name="us-west-2").get_item = mock_get_item

        # Run the test function
        result = func(*args, **kwargs)

        print("RESTORING")

        # Restore original methods
        boto3.client("dynamodb", region_name="us-west-2").put_item = original_put_item
        boto3.client("dynamodb", region_name="us-west-2").get_item = original_get_item

        # Calculate and print costs
        write_cost = awstimator.calculate_req_wcu(write_size)
        read_cost = awstimator.calculate_req_rcu(read_size)
        print(f"\nDynamoDB operation costs:")
        print(f"Write: {write_size} bytes, {write_cost:.2f} WCU")
        print(f"Read: {read_size} bytes, {read_cost:.2f} RCU")

        return result

    return wrapper
