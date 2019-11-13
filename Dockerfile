# Ubuntu Linux as the base imag
FROM ubuntu:16.04

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install packages 
RUN apt-get -y update && \
    apt-get -y upgrade && \
	apt-get -y install python3-pip python3-dev &&\
	pip3 install spacy 

# Add the files
ADD . /QA

WORKDIR /QA

CMD ["chmod 777 ask"]
CMD ["chmod 777 answer"]

ENTRYPOINT ["/bin/bash", "-c"]