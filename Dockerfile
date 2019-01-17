FROM docker.elastic.co/beats/filebeat:6.4.3

LABEL MAINTAINER="roberto cardenas <rcardenas20@gmail.com>"

USER root
RUN yum --enablerepo=extras install epel-release -y && \
    yum update -y && \
    yum install python-pip -y && \
    pip install --upgrade pip && \
    pip install requests && \
    yum clean all && \
    rm -rf /var/cache/yum

ENV LOGS_PATH=/var/log/jira \
    DATA_PATH=/opt/jira/data \
    FILEBEAT_HOME=/usr/share/filebeat \
    APPLICATION_HOME=/opt/agile_portafolio \
    PERIOD=30s

COPY ./filebeat/filebeat.yml ${FILEBEAT_HOME}/filebeat.yml
ADD ./source ${APPLICATION_HOME}
ADD entrypoint.sh /entrypoint.sh
RUN mkdir -p ${LOGS_PATH} && \
    mkdir -p ${DATA_PATH} && \
    chown filebeat:filebeat ${LOGS_PATH}} && \
    chown filebeat:filebeat ${DATA_PATH} && \
    chown filebeat:filebeat ${FILEBEAT_HOME}/filebeat.yml && \
    chown -R filebeat:filebeat ${APPLICATION_HOME} && \
    chown filebeat:filebeat /entrypoint.sh && \
    chmod go-w /usr/share/filebeat/filebeat.yml && \
    chmod +x /entrypoint.sh
USER filebeat

ENTRYPOINT  ["/entrypoint.sh"]
CMD ["start"]