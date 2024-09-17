import boto3
from moto import mock_aws
import pytest
from .ddb_cost_decorator import measure_ddb_cost

@pytest.fixture
@mock_aws
def dynamodb_mock_sock():
    # return boto3.client("dynamodb", region_name="us-west-2")
    yield boto3.client("dynamodb", region_name="us-west-2")
    # yield boto3.resource("dynamodb")

@measure_ddb_cost
# @mock_aws
def test_put_item_with_streams(dynamodb_mock_sock):
    print("TEST --> test_put_item_with_streams")
    name = "TestTable"
    # conn = boto3.client(
    #     "dynamodb",
    #     region_name="us-west-2",
    #     # aws_access_key_id="ak",
    #     # aws_secret_access_key="sk",
    # )
    conn = dynamodb_mock_sock

    conn.create_table(
        TableName=name,
        KeySchema=[{"AttributeName": "forum_name", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "forum_name", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    # The decorator will automatically measure the cost of this write operation
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

    # The decorator will automatically measure the cost of this read operation
    result = conn.get_item(TableName=name, Key={"forum_name": {"S": "Fancy Forum"}})

    assert result["Item"] == {
        "forum_name": {"S": "Fancy Forum"},
        "subject": {"S": "Check this out!"},
        "Body": {"S": "http://url_to_cat.gif"},
        "SentBy": {"S": "test"},
        "Data": {"M": {"Key1": {"S": "Value1"}, "Key2": {"S": "Value2"}}},
    }


def test_example_test_measuring_cost():
    assert 1 == 1
