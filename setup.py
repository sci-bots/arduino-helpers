#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from setuptools import setup
import sys

# add the current directory as the first listing on the python path
# so that we import the correct version.py
sys.path.insert(0, '.')
import version


setup(name='arduino-helpers',
      version=version.getVersion(),
      description='Helper functions for reading configs, etc. from an '
      'installed Arduino directory.',
      author='Christian Fobel',
      author_email='christian@fobel.net',
      url='http://github.com/wheeler-microfluidics/arduino-helpers.git',
      license='GPLv2',
      install_requires=['serial_device', 'path_helpers'],
      packages=['arduino_helpers', 'arduino_helpers.hardware',
                'arduino_helpers.bin'],
      include_package_data=True)
