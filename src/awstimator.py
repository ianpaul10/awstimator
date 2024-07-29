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
        # deserialier = boto3.dynamodb.types.TypeDeserializer()
        serializer = TypeSerializer()
        ddb_obj = {k: serializer.serialize(v) for k, v in base_obj.items()}
        return ddb_obj

    def estimate_cost_of_write(self, json_obj, is_ddb_obj=False) -> float:
        test_item = {
            "id": {"S": "f0ba8d6c"},
            "fullName": {"S": "Ian Paul"},
            "isAdmin": {"BOOL": "true"},
            "favouriteNumber": {"N": "-1E-130"},
            "foods": {
                "SS": [
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                    "pizza",
                    "burger",
                ]
            },
        }
        encoded_json_str = str(json.dumps(test_item)).encode(
            encoding="ascii", errors="replace"
        )

        actual_size = calculate_item_size_in_bytes(test_item)

        print(actual_size)

        print(f"utf-8: {len(encoded_json_str)}")
        return len(encoded_json_str)


if __name__ == "__main__":
    print("AWStimator")
    Awstimator().estimate_cost_of_write("test")
