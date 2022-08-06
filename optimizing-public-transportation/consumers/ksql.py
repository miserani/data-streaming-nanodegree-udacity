"""Configures KSQL to combine station and turnstile data"""
import json
import logging

import requests

import topic_check


logger = logging.getLogger(__name__)


KSQL_URL = "http://0.0.0.0:8088"

#
# TODO: Complete the following KSQL statements.
# TODO: For the first statement, create a `turnstile` table from your turnstile topic.
#       Make sure to use 'avro' datatype!
# TODO: For the second statment, create a `turnstile_summary` table by selecting from the
#       `turnstile` table and grouping on station_id.
#       Make sure to cast the COUNT of station id to `count`
#       Make sure to set the value format to JSON

KSQL_STATEMENT = """
create table TURNSTILE_EVENTS (
    STATION_ID BIGINT primary key,
    STATION_NAME STRING,
    LINE STRING
) with (
    KAFKA_TOPIC = 'com.transitchicago.station.turnstiles',
    KEY_FORMAT = 'AVRO',
    PARTITIONS = 2,
    VALUE_FORMAT = 'JSON'
);

CREATE TABLE turnstile_summary
WITH (VALUE_FORMAT = 'JSON_SR') AS
    SELECT 
        station_id as STATION_ID, 
        COUNT(*) AS count
    FROM turnstile_event
    GROUP BY station_id;
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
