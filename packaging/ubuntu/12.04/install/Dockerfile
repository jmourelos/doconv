FROM ubuntu:12.04

# doconv plugin dependencies
RUN apt-get install -y rubygems asciidoc
RUN gem install asciidoctor

# install pip
RUN sed -i 's/precise main/precise main universe multiverse/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y python-pip

# install doconv dependencies
RUN apt-get install -y python-lxml python-networkx

# install doconv
RUN pip install doconv
