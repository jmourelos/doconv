FROM base/archlinux:latest

RUN pacman -Sy --noconfirm


# disable signature checking
RUN sed -i 's/^SigLevel.*$/SigLevel = Never/g' /etc/pacman.conf

# install python
RUN pacman --noconfirm -S python2

# install packer to ease installation of AUR packages
RUN pacman --noconfirm -S binutils jshon expac git
