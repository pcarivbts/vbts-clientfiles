"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.

    Usage: fab dev|lab deploy
"""

from fabric.api import cd, local, env, run, require, put, lcd, prefix
from fabric.context_managers import settings
from fabric.operations import sudo

from commands.python_packaging import package_python_pcari_dictionary

env.pkgfmt = "deb"
env.gsmeng = "osmocom"
env.depmap = {}
env.path = "~/vbts-clientfiles"


def dev():
    """ Host config for local Vagrant VM. """
    with lcd('../'):
        host = local('vagrant ssh-config %s | grep HostName' % (env.gsmeng,),
                     capture=True).split()[1]
        port = local('vagrant ssh-config %s | grep Port' % (env.gsmeng,),
                     capture=True).split()[1]
        env.hosts = ['vagrant@%s:%s' % (host, port)]
        identity_file = local('vagrant ssh-config %s | grep IdentityFile' %
                              (env.gsmeng,), capture=True)
        env.key_filename = identity_file.split()[1].strip('"')


def lab():
    """ Host config for real hardware, lab version (i.e., default login). """
    env.hosts = ['endaga@192.168.1.25']
    env.password = 'endaga'


def deploy():
    """
    Deploy the latest version of the site to the servers,
    install any required third party modules,
    install the virtual host and then restart the webserver
    """
    require('hosts', provided_by=[dev, lab])
    sudo('mkdir -p ~/vbts-clientfiles')
    install_deb_packages()
    install_other_packages()


def install_deb_packages():
    package_deb()
    update_deb()


def install_other_packages():
    require('path', provided_by=[deploy])
    with cd('~/client/vbts-clientfiles'):
        sudo('chmod +x package_apps.sh')
        sudo('./package_apps.sh')

        sudo('chmod +x install_apps.sh')
        sudo('./install_apps.sh')

        sudo('chmod +x copyme.sh')
        sudo('./copyme.sh')


def package_deb():
    package_python_pcari_dictionary()
    print 'packaging complete.'


def update_deb(flush_cache='no'):
    """ Installs all the packages in ~/vbts-clientfiles.
    """
    bin_path = 'dists/localdev/main/binary-i386'
    if (env.gsmeng == "osmocom"):
        bin_path = 'dists/localdev/main/binary-amd64'

    with cd('~/vbts-clientfiles'):
        if flush_cache == 'yes':
            run('rm -rf %s || exit 0' % bin_path)
            run('mkdir -p %s' % bin_path)
            run('apt-ftparchive packages . '
                '> %s/Packages' % bin_path)
            with cd('%s' % bin_path):
                run('gzip -c Packages > Packages.gz')
                run('apt-ftparchive '
                    '-o APT::FTPArchive::Release::Components=main release . '
                    '> Release')
            with cd('dists/localdev/'):
                run('apt-ftparchive '
                    '-o APT::FTPArchive::Release::Codename=localdev '
                    '-o APT::FTPArchive::Release::Components=main release . '
                    '> Release')
            run('sudo apt-get update')
        run('for filename in *.deb; do echo y '
            '| sudo gdebi --option=APT::Default-Release=localdev '
            '--option=Dpkg::Options::="--force-overwrite" -q $filename '
            '|| exit 1;  done')
