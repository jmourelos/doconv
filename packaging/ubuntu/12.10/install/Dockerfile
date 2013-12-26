FROM ubuntu:12.10

RUN apt-get update

# doconv plugin dependencies
RUN apt-get install --no-install-recommends -y asciidoc

RUN apt-get install -y software-properties-common

RUN add-apt-repository -y ppa:doconv-py/ppa
