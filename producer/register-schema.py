import datetime

from pydantic import BaseModel
from schema_registry.client import SchemaRegistryClient

client = SchemaRegistryClient(url="http://127.0.0.1:8081")


class User(BaseModel):
    ts: datetime.datetime
    name: str
    country: str
    age: int


schema_id = client.register("USERS-key", User.schema_json(), schema_type="JSON")

print(schema_id)

# result = client.check_version("user", User.schema_json(), schema_type="JSON")
# print(result)
#
# compatibility = client.test_compatibility(
#     "user", User.schema_json(), schema_type="JSON"
# )
# print(compatibility)
