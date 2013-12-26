FROM ubuntu:12.10

RUN apt-get update

RUN apt-get install -y apt-file python-support debhelper

RUN apt-get install -y python-pip

RUN pip install stdeb

RUN apt-file update

# install devscripts (provides debuild)
# installation of devscripts requires a workaround to work under docker
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -s /bin/true /sbin/initctl

RUN apt-get install -y devscripts


RUN mkdir -p /.gnupg
RUN mkdir -p /tmp/doconv/{build,install,sources}

