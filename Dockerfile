FROM ubuntu 
MAINTAINER Tim Pizey <tim@pizey.net>

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y libpq-dev && \
    apt-get install -y git && \
    apt-get install -y python-dev && \
    apt-get install -y python-pip && \
    apt-get clean 



RUN mkdir membership
ADD . membership/


RUN cd membership && \
#    pip install virtualenv && \
#    virtualenv venv && \
#    . venv/bin/activate && \
    pip install -r requirements.txt 

RUN cd membership && \
    ./redo.sh

CMD bash
