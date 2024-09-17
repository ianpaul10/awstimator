import json

from pydantic import BaseModel, Field


class Config(BaseModel):

    pricing_model: str = Field(default="on_demand")
    writes_per_month: int = Field(default=10000)
    reads_per_month: int = Field(default=10000)

    wcu_item_size_bytes: int = Field(default=1000)
    rcu_item_size_bytes: int = Field(default=4 * 1000)

    @classmethod
    def from_default(cls):
        with open("default_config.json", "r") as f:
            config = json.load(f)
            return cls(**config)

    @classmethod
    def from_file(cls, config_file_path):
        with open(config_file_path, "r") as f:
            config = json.load(f)
            return cls(**config)
