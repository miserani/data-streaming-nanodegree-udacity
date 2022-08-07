#echo 'schema.registry.url=http://localhost:8081' >> /etc/kafka/connect-distributed.properties

## Topics
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.addison"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.austin"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.belmont"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.california"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.chicago"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.cicero"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.clark_and_lake"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.clinton"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.cumberland"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.damen"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.division"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.forest_park"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.grand"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.harlem"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.illinois_medical_district"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.irving_park"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.jackson"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.jefferson_park"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.kedzie_homan"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.lasalle"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.logan_square"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.monroe"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.montrose"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.oak_park"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.ohare"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.pulaski"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.racine"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.rosemont"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.uic_halsted"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.washington"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.western_and_forest_pk_branch"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.arrivals.western_and_ohare_branch"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.weather"
kafka-topics --delete --bootstrap-server localhost:29092 --topic "com.transitchicago.station.turnstiles"
kafka-topics --create --topic "com.transitchicago.station.weather" --partitions 1 --replication-factor 1 --bootstrap-server localhost:29092 > /tmp/startup.log 2>&1
kafka-topics --create --topic "com.transitchicago.station.turnstiles" --partitions 1 --replication-factor 1 --bootstrap-server localhost:29092 > /tmp/startup.log 2>&1

## Configure the directory structure for KSQL
mkdir -p /var/lib/kafka-streams
chmod g+rwx /var/lib/kafka-streams
chgrp -R confluent /var/lib/kafka-streams
