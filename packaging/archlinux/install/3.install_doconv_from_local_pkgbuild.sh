mkdir -p /build_out
cd /build_out

#/tmp/doconv/build/PKGBUILD
packer-aur --noconfirm -S python2-networkx
sudo -u builduser bash -c 'cd /tmp/doconv/build/ && makepkg --force --noconfirm -s'
mv /tmp/doconv/build/*.pkg.tar.xz /build_out
pacman -U --noconfirm /build_out/*.pkg.tar.xz
