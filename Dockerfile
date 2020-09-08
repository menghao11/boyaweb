FROM docker.io/centos
WORKDIR /var/IntelPerf

COPY hello.py /var/IntelPerf/
RUN mkdir templates
COPY templates/ /var/IntelPerf/templates/
COPY run.sh /var/IntelPerf

RUN yum install -y python36
RUN chmod 777 run.sh \
    && pip3 install flask \
    && pip3 install requests

EXPOSE 5000

ENTRYPOINT  ["./run.sh"]
