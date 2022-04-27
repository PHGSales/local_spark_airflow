FROM apache/airflow:2.1.0-python3.6
USER root

RUN apt update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get install -y libpq-dev python-dev && \
    apt-get install -y libzbar-dev && \
    apt-get clean;

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

USER airflow
COPY docker-requirements.txt.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r docker-requirements.txt.txt
