"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.

-
Fabric commands related to python packaging.
"""

import imp
import json
import os.path

from fabric.api import cd, env, execute, run, sudo
from fabric.context_managers import shell_env
from fabric.contrib.files import exists
from fabric.operations import get
from fabric.operations import put

env.pkgfmt = "deb"
env.sources_dir = "/home/vagrant/client/vbts-clientfiles/apps"
env.packages_dir = "~/vbts-clientfiles"


def package_python_pcari_dictionary(package_requirements='no'):
    name = 'dictionary'
    path = os.path.join(env.sources_dir, name)
    with cd(path):
        run('fpm -s python -t %s'
            ' --depends dict-moby-thesaurus'
            ' --depends dict-wn'
            ' setup.py' % env.pkgfmt)
        print ('mv *.%s %s/' % (env.pkgfmt, env.packages_dir))
        sudo('mv *.%s %s/' % (env.pkgfmt, env.packages_dir))


def package_python_pcari_twits(package_requirements='no'):
    name = 'twits'
    path = os.path.join(env.sources_dir, name)
    with cd(path):
        run('fpm -s python -t %s'
            ' setup.py' % env.pkgfmt)
        run('mv *.%s %s' % (env.pkgfmt, env.packages_dir))


def package_python_pcari_filereader(package_requirements='no'):
    name = 'filereader'
    path = os.path.join(env.sources_dir, name)
    with cd(path):
        run('fpm -s python -t %s'
            ' setup.py' % env.pkgfmt)
        run('mv *.%s %s' % (env.pkgfmt, env.packages_dir))


def package_python_pcari_rss(package_requirements='no'):
    name = 'rss'
    path = os.path.join(env.sources_dir, name)
    with cd(path):
        run('fpm -s python -t %s'
            ' setup.py' % env.pkgfmt)
        run('mv *.%s %s' % (env.pkgfmt, env.packages_dir))
