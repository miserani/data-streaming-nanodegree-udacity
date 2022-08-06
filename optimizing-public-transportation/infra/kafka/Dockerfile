FROM confluentinc/ksqldb-server:0.24.0

USER root

RUN wget https://repo1.maven.org/maven2/junit/junit/4.12/junit-4.12.jar -P share/java/confluent-hub-client/ & \
    wget https://repo1.maven.org/maven2/org/hamcrest/hamcrest-all/1.3/hamcrest-all-1.3.jar -P share/java/confluent-hub-client/

RUN ls -l share/java/confluent-hub-client

USER appuser