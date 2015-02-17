FROM ubuntu 
MAINTAINER Tim Pizey <tim@pizey.net>

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y python-dev && \
    apt-get install -y python-pip && \
    apt-get install -y texlive && \
    apt-get install -y texlive-latex-extra && \
    apt-get clean 

RUN mkdir membership
ADD . membership/

RUN cd membership && pip install -r requirements.txt 

EXPOSE 8000
WORKDIR membership
RUN ./redo.sh


