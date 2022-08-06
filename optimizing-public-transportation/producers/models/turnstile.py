"""Creates a turnstile data producer"""
import logging
from pathlib import Path

from confluent_kafka import avro

from producers.models.producer import Producer
from producers.models.turnstile_hardware import TurnstileHardware

logger = logging.getLogger(__name__)


class Turnstile(Producer):
    key_schema = avro.load(f"{Path(__file__).parents[0]}/schemas/turnstile_key.json")

    value_schema = avro.load(
        f"{Path(__file__).parents[0]}/schemas/turnstile_value.json"
    )

    def __init__(self, station):
        """Create the Turnstile"""
        station_name = (
            station.name.lower()
                .replace("/", "_and_")
                .replace(" ", "_")
                .replace("-", "_")
                .replace("'", "")
        )

        topic_name = "com.transitchicago.station.turnstiles"
        super().__init__(
            f"{topic_name}",
            key_schema=Turnstile.key_schema,
            value_schema=Turnstile.value_schema,
            num_partitions=3,
        )
        self.station = station
        self.turnstile_hardware = TurnstileHardware(station)

    def run(self, timestamp, time_step):
        """Simulates riders entering through the turnstile."""
        num_entries = self.turnstile_hardware.get_entries(timestamp, time_step)
        logger.info("turnstile kafka integration incomplete - skipping")

        logger.info("arrival kafka integration incomplete - skipping")
        while num_entries > 0:
            self.producer.produce(
                topic=self.topic_name,
                key={"timestamp": int(timestamp.timestamp() * 1000)},
                value={
                    "station_id": int(self.station.station_id),
                    "station_name": self.station.name,
                    "line": str(self.station.color),
                }
            )
            num_entries = --num_entries
