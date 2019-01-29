doconv_version=0.1.7

build_out=/build_out

mkdir -p $build_out
cp /tmp/doconv/sources/doconv-$doconv_version\.tar.gz $build_out

# --ignore-install-requires to keep track of dependencies manually. The file
# stdeb.conf will be used.
py2dsc --ignore-install-requires --dist-dir $build_out --extra-cfg-file /tmp/doconv/build/stdeb.cfg $build_out/doconv-$doconv_version\.tar.gz
if [ "$?" == 0 ]; then
    doconv_dir=$(ls -d $build_out/doconv-*)
    cd $doconv_dir
    dpkg-buildpackage -rfakeroot -uc -us
    doconv_deb=$(ls $build_out/python-doconv*.deb)
    cp $doconv_deb /tmp/doconv/sources
fi


