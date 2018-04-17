#!/bin/sh

#Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
#The Village Base Station Project (PCARI-VBTS). All rights reserved.
#
#This source code is licensed under the BSD-style license found in the
#LICENSE file in the root directory of this source tree.

echo "Copying FreeSwitch XML chatplan files"
sudo cp ./xml/chatplan/* /etc/freeswitch/chatplan/default/

echo "Copying FreeSwitch XML dialplan files"
sudo cp ./xml/dialplan/* /etc/freeswitch/dialplan/default/

echo "Copying FreeSwitch scripts"
sudo cp ./scripts/* /usr/share/freeswitch/scripts/


echo "Copying edits to core"
sudo cp ./core/billing.py /usr/local/lib/python2.7/dist-packages/core/

echo "Copying edits to federer_handlers"
sudo cp ./core/sms.py /usr/local/lib/python2.7/dist-packages/core/federer_handlers/
sudo cp ./core/sms_cdr.py /usr/local/lib/python2.7/dist-packages/core/federer_handlers/
sudo cp ./core/cdr.py /usr/local/lib/python2.7/dist-packages/core/federer_handlers/
sudo cp ./core/registration.py /usr/local/lib/python2.7/dist-packages/core/federer_handlers/

echo "Give django permission to write to FS XMLplan dirs"
sudo chown root:www-data /etc/freeswitch/chatplan/default
sudo chown root:www-data /etc/freeswitch/dialplan/default

sudo pycompile /usr/local/lib/python2.7/dist-packages/core

