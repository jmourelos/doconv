build_out=/build_out
mkdir $build_out
cd $build_out

makepkg --force --source --noconfirm --syncdeps -p /tmp/doconv/build/PKGBUILD
doconv_src_package=$(ls $build_out/doconv-*.src.tar.gz)
cp $doconv_src_package /tmp/doconv/sources

echo "Package can be found in /tmp/doconv/sources/"
