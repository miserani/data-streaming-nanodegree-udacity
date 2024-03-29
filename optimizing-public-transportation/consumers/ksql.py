"""Configures KSQL to combine station and turnstile data"""
import json
import logging

import requests

import topic_check


logger = logging.getLogger(__name__)


KSQL_URL = "http://localhost:8088"

KSQL_STATEMENT = """
CREATE TABLE TURNSTILE (
     STATION_ID BIGINT PRIMARY KEY,
     STATION_NAME VARCHAR,
     LINE VARCHAR
   ) WITH (
    KAFKA_TOPIC = 'com.transitchicago.station.turnstiles',
    KEY_FORMAT = 'AVRO',
    VALUE_FORMAT = 'AVRO',
    PARTITIONS = 1
);

CREATE TABLE TURNSTILE_SUMMARY
WITH (VALUE_FORMAT = 'JSON') AS
    SELECT 
        STATION_ID AS STATION_ID, 
        COUNT(*) AS COUNT
    FROM TURNSTILE
    GROUP BY STATION_ID;
"""


def execute_statement():
    """Executes the KSQL statement against the KSQL API"""
    if topic_check.topic_exists("TURNSTILE_SUMMARY") is True:
        return

    logging.debug("executing ksql statement...")

    resp = requests.post(
        f"{KSQL_URL}/ksql",
        headers={"Content-Type": "application/vnd.ksql.v1+json"},
        data=json.dumps(
            {
                "ksql": KSQL_STATEMENT,
                "streamsProperties": {"ksql.streams.auto.offset.reset": "earliest"},
            }
        ),
    )

    # Ensure that a 2XX status code was returned
    resp.raise_for_status()


if __name__ == "__main__":
    execute_statement()
