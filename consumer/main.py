import json
import json
import os

from kafka import KafkaConsumer
from pydantic import BaseModel
from schema_registry.client import SchemaRegistryClient

BOOTSTRAP_SERVERS = (
    "kafka:9092" if os.getenv("RUNTIME_ENVIRONMENT") == "DOCKER" else "localhost:9092"
)

TOPIC = "USERS"

class User(BaseModel):
    ts: str
    name: str
    country: str
    age: int = None

def consume_messages():
    consumer = KafkaConsumer(
        TOPIC,
        auto_offset_reset="earliest",
        bootstrap_servers=BOOTSTRAP_SERVERS,
    )

    client = SchemaRegistryClient(url="http://127.0.0.1:8081")

    average_age = 0
    user_count = 0
    for msg in consumer:
        idx, value = msg.key.decode("utf-8"), json.loads(msg.value)
        user = User(**value)

        compatibility = client.test_compatibility("USERS-value", user.schema_json(), schema_type="JSON")
        if not compatibility:
            raise Exception("Schema is not compatible with the latest version")

        average_age = (average_age * user_count + int(value["age"])) // (user_count + 1)
        user_count += 1

        print(
            f"{value} \n| Average age: {average_age} | User count: {user_count}\n"
        )


if __name__ == "__main__":
    consume_messages()
