#!/usr/bin/env python
from distutils.core import setup

setup(name='arduino_helpers',
    version='0.0.1',
    description='Helper functions for reading configs, etc. from an installed '
                'Arduino directory.',
    keywords='arduino build config',
    author='Christian Fobel',
    url='https://github.com/cfobel/arduino_helpers',
    license='GPL',
    packages=['arduino_helpers', 'arduino_helpers.hardware'],
)
