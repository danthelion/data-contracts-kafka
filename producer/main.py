import datetime
import json
import os
from time import sleep

from faker import Faker
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
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
    # age: int
    date_of_birth: str


def create_topic_if_not_exists():
    admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
    if TOPIC not in admin_client.list_topics():
        admin_client.create_topics(
            [NewTopic(name=TOPIC, num_partitions=1, replication_factor=1)]
        )


def push_messages():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
    )
    fake = Faker()

    client = SchemaRegistryClient(url="http://127.0.0.1:8081")

    for i in range(100):
        data = User(
            ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            name=fake.name(),
            country=fake.country(),
            date_of_birth=str(fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=100)),
            # age=fake.random_int(min=0, max=100),
        )
        # Get the latest schema from the registry and serialize the message with it
        compatibility = client.test_compatibility("USERS-value", data.schema_json(), schema_type="JSON")
        if not compatibility:
            raise Exception("Schema is not compatible with the latest version")

        producer.send(topic=TOPIC, key=str(i).encode("utf-8"), value=json.dumps(data.dict()).encode("utf-8"))
        print(f"Sent message {i} -> {data}")
        sleep(2)


if __name__ == "__main__":
    create_topic_if_not_exists()
    push_messages()
