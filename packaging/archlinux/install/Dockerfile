FROM base/arch:latest

RUN pacman -Sy

# disable signature checking
RUN sed -i 's/^SigLevel.*$/SigLevel = Never/g' /etc/pacman.conf

# install python
RUN pacman --noconfirm -S python2

# install packer to ease installation of AUR packages
RUN pacman --noconfirm -S binutils jshon expac git
RUN curl https://aur.archlinux.org/packages/pa/packer/PKGBUILD -o PKGBUILD
RUN makepkg
RUN pacman --noconfirm -U packer-*.pkg.tar.xz

# doconv plugin dependencies
RUN pacman --noconfirm -S asciidoc

# create directories to share with host
RUN mkdir -p /tmp/doconv/{build,install}
