#Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
#The Village Base Station Project (PCARI-VBTS). All rights reserved.
#
#This source code is licensed under the BSD-style license found in the
#LICENSE file in the root directory of this source tree.

cd apps
for d in *
do
    echo "$d"
    cd $d
    echo "Installing app: $d"
    sudo python setup.py install
    cd ..
done
