FROM base/archlinux:latest

RUN pacman -Sy --noconfirm

# disable signature checking
RUN sed -i 's/^SigLevel.*$/SigLevel = Never/g' /etc/pacman.conf

# install python
RUN pacman --noconfirm -S python2

# install packer to ease installation of AUR packages
RUN pacman --noconfirm -S binutils jshon expac git




RUN pacman -S --needed --noconfirm sudo fakeroot
RUN useradd builduser -m
RUN passwd -d builduser
RUN printf 'builduser ALL=(ALL) ALL\n' | tee -a /etc/sudoers # Allow the builduser passwordless sudo
RUN sudo -u builduser bash -c 'cd ~ && curl "https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=packer-aur-git" -o PKGBUILD && makepkg -s --noconfirm'


RUN pacman --noconfirm -U /home/builduser/packer-*.pkg.tar.xz

# doconv plugin dependencies
RUN pacman --noconfirm -S asciidoc

# create directories to share with host
RUN mkdir -p /tmp/doconv/{build,install}
