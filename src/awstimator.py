from decimal import Decimal
import json
import boto3
from config import Config
from ddb_size_calc import calculate_item_size_in_bytes
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer


class Awstimator:
    def __init__(self) -> None:
        # self.boto_ddb = boto3.resource("dynamodb")
        self.config = Config

    @staticmethod
    def _convert_to_ddb_obj(base_obj: dict):
        serializer = TypeSerializer()

        ddb_obj = {}

        for k, v in base_obj.items():
            if isinstance(v, float):
                v = Decimal(str(v))
            ddb_obj[k] = serializer.serialize(v)
        return ddb_obj

    def get_size_in_bytes(self, item, is_ddb_item=False) -> int:
        """
        Returns the number of bytes required to store the item in DynamoDB.

        Base on https://medium.com/@zaccharles/d1728942eb7c

        :param item: ddb item
        :type item: dict
        :param is_ddb_item: true if it's in the standard ddb format, defaults to False
        :type is_ddb_item: bool, optional
        :return: bytes
        :rtype: int
        """

        if not is_ddb_item:
            item = self._convert_to_ddb_obj(item)

        actual_size = calculate_item_size_in_bytes(item)

        return actual_size["size"]

    def calculate_req_rcu(self, item_size_bytes: int) -> float:
        return item_size_bytes / Config.rcu_item_size_bytes

    def calculate_req_wcu(self, item_size_bytes: int) -> float:
        return item_size_bytes / Config.wcu_item_size_bytes


if __name__ == "__main__":
    print("AWStimator")

    default_non_ddb_obj = {
        "id": "sadfasdggasdfasdfsadfsadfasdf",
        "fullName": "Ian Paul",
        "isAdmin": True,
        "favouriteNumber": -1e-130,
        "otherNumber": 3.141592653589793,
        "foods": {"pizza", "burger", "beer"},
    }

    default_obj = {
        "id": {"S": "sadfasdggasdfasdfsadfsadfasdf"},
        "fullName": {"S": "Ian Paul"},
        "isAdmin": {"BOOL": True},
        "favouriteNumber": {"N": "-1E-130"},
        "otherNumber": {"N": "3.141592653589793"},
        "foods": {"SS": ["pizza", "burger", "beer"]},
    }

    size_x = Awstimator().get_size_in_bytes(item=default_non_ddb_obj, is_ddb_item=False)
    print(size_x)
    size_y = Awstimator().get_size_in_bytes(item=default_obj, is_ddb_item=True)
    print(size_y)

    assert size_x == size_y
