FROM ubuntu 
MAINTAINER Tim Pizey <tim@pizey.net>

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y python-dev && \
    apt-get install -y python-pip && \
    apt-get install -y latex & \
    apt-get clean 

RUN mkdir membership
ADD . membership/

WORKDIR membership
RUN pip install -r requirements.txt 

RUN ./redo.sh


