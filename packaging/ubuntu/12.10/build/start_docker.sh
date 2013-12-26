docker run -i -t \
-v $DOCONV_DEV_DIR/dist/:/tmp/doconv/sources \
-v $DOCONV_DEV_DIR/packaging/ubuntu/12.10/build:/tmp/doconv/build \
-v $DOCONV_DEV_DIR/packaging/ubuntu/12.10/install:/tmp/doconv/install \
-v $HOME/.gnupg:/.gnupg \
doconv/ubuntu-12.10-build \
/bin/bash
