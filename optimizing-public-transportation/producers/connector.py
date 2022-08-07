"""Configures a Kafka Connector for Postgres Station data"""
import json
import logging

import requests
from requests import HTTPError

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


KAFKA_CONNECT_URL = "http://localhost:8083/connectors"
CONNECTOR_NAME = "stations"


def configure_connector():
    """Starts and configures the Kafka Connect connector"""
    logging.debug("creating or updating kafka connect connector...")

    resp = requests.get(f"{KAFKA_CONNECT_URL}/{CONNECTOR_NAME}")
    if resp.status_code == 200:
        logging.debug("connector already created skipping recreation")
        return
    # To delete a misconfigured connector: CURL -X DELETE localhost:8083/connectors/stations
    resp = requests.post(
       KAFKA_CONNECT_URL,
       headers={"Content-Type": "application/json"},
       data=json.dumps({
           "name": CONNECTOR_NAME,
           "config": {
               "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
               "key.converter": "org.apache.kafka.connect.json.JsonConverter",
               "value.converter": "org.apache.kafka.connect.json.JsonConverter",
               "key.converter.schemas.enable": "false",
               "value.converter.schemas.enable": "false",
               "batch.max.rows": "100",
               "connection.url": "jdbc:postgresql://localhost:5432/cta",
               "connection.user": "guest",
               "connection.password": "guest",
               "table.whitelist": "stations",
               "mode": "incrementing",
               "incrementing.column.name": "stop_id",
               "topic.prefix": "com.transitchicago.station.",
               "poll.interval.ms": "60000",
           }
       }),
    )

    ## Ensure a healthy response was given
    try:
        resp.raise_for_status()
    except HTTPError as e:
        logger.error("connector code not completed skipping connector creation", e)
        raise e
    logging.debug("connector created successfully")


if __name__ == "__main__":
    configure_connector()
