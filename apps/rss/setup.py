"""
Copyright (c) 2015-present, Philippine-California Advanced Research Institutes-
The Village Base Station Project (PCARI-VBTS). All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from setuptools import setup

VERSION = '1.0'
setup(
    name='pcarirss',
    author='PCARI-VBTS',
    author_email='pcari.vbts@gmail.com',
    version=VERSION,
    description='PCARI-VBTS RSS Plugin',
    packages=['pcarirss'],
    license='BSD',
    long_description=open('README.md').read(),
    install_requires=[
        "feedparser==5.2.1",
    ],
    include_package_data=True,
    data_files=[
        ('/usr/share/freeswitch/scripts', [
            'fs_script/PCARI_RSS.py',
        ])
    ],
)
