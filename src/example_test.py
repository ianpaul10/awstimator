import boto3
import moto
import pytest


@pytest.fixture
@moto.mock_aws
def dynamodb_mock():
    yield boto3.resource("dynamodb")
    # with moto.mock_dynamodb():
    #     yield boto3.resource('dynamodb')


@moto.mock_aws
def test_put_item_with_streams():
    name = "TestTable"
    conn = boto3.client(
        "dynamodb",
        region_name="us-west-2",
        aws_access_key_id="ak",
        aws_secret_access_key="sk",
    )

    conn.create_table(
        TableName=name,
        KeySchema=[{"AttributeName": "forum_name", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "forum_name", "AttributeType": "S"}],
        # StreamSpecification={
        #     "StreamEnabled": True,
        #     "StreamViewType": "NEW_AND_OLD_IMAGES",
        # },
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    conn.put_item(
        TableName=name,
        Item={
            "forum_name": {"S": "Fancy Forum"},
            "subject": {"S": "Check this out!"},
            "Body": {"S": "http://url_to_cat.gif"},
            "SentBy": {"S": "test"},
            "Data": {"M": {"Key1": {"S": "Value1"}, "Key2": {"S": "Value2"}}},
        },
    )

    result = conn.get_item(TableName=name, Key={"forum_name": {"S": "Fancy Forum"}})

    assert result["Item"] == {
        "forum_name": {"S": "Fancy Forum"},
        "subject": {"S": "Check this out!"},
        "Body": {"S": "http://url_to_cat.gif"},
        "SentBy": {"S": "test"},
        "Data": {"M": {"Key1": {"S": "Value1"}, "Key2": {"S": "Value2"}}},
    }


@moto.mock_aws
@pytest.mark.skip
def test_dynamodb_add_and_read_item():
    # Create connection to the mock dynamodb
    conn = boto3.client("dynamodb", region_name="us-west-2")

    # Create a mock table
    table = conn.create_table(
        TableName="TestTable",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    # Add an item to the table
    item = {"id": "1", "name": "Test Item", "value": 100}
    table.put_item(Item=item)

    # Read the item back
    response = table.get_item(Key={"id": "1"})
    retrieved_item = response["Item"]

    # Assert on the contents
    assert retrieved_item["id"] == "1"
    assert retrieved_item["name"] == "Test Item"
    assert retrieved_item["value"] == 100


def test_example_test_measuring_cost():
    assert 1 == 1
