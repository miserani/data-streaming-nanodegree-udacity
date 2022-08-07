"""Producer base-class providing common utilites and functionality"""
import logging
import time


from confluent_kafka import avro, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer

logger = logging.getLogger(__name__)

SCHEMA_REGISTRY_URL = "http://localhost:8081"
BROKER_URL = "PLAINTEXT://localhost:29092"


def is_topic_exists(client, topic):
    topic_metadata = client.list_topics(timeout=2)
    return topic in set(t.topic for t in iter(topic_metadata.topics.values()))


class Producer:
    """Defines and provides common functionality amongst Producers"""

    # Tracks existing topics across all Producer instances
    existing_topics = set([])

    def __init__(
        self,
        topic_name,
        key_schema,
        value_schema=None,
        num_partitions=1,
        num_replicas=1,
        auto_create=False,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas

        self.broker_properties = {
            "bootstrap.servers": BROKER_URL,
            "schema.registry": SCHEMA_REGISTRY_URL,
            "auto.create.topics.enable": auto_create,
        }

        self.client = AdminClient({"bootstrap.servers": BROKER_URL})

        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        self.producer: AvroProducer = AvroProducer(
            {
                "bootstrap.servers": BROKER_URL,
                "schema.registry.url": SCHEMA_REGISTRY_URL,
            },
            default_key_schema=self.key_schema,
            default_value_schema=self.value_schema,
        )

    def create_topic(self):
        """Creates the producer topic if it does not already exist"""
        topics = self.client.create_topics(
            [
                NewTopic(
                    topic=self.topic_name,
                    num_partitions=self.num_partitions,
                    replication_factor=self.num_replicas,
                    config={
                        "cleanup.policy": "delete",
                        "compression.type": "lz4",
                        "delete.retention.ms": "2000",
                        "file.delete.delay.ms": "2000",
                    },
                )
            ]
        )
        for topic, future in topics.items():
            try:
                if is_topic_exists(self.client, topic):
                    logger.info(f"topic {topic} exists")
                    return
                future.result()
                logger.info(f"topic {topic} created")
            except KafkaException as e:
                logger.warning(
                    f"topic {topic} creation kafka integration incomplete - skipping"
                )

    def time_millis(self):
        return int(round(time.time() * 1000))

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""
        #
        #
        # TODO: Write cleanup code for the Producer here
        #
        #
        self.producer.flush()
        logger.info("producer close incomplete - skipping")

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
