from paver.easy import task, needs
from paver.setuputils import setup

import os
import sys

# add the current directory as the first listing on the python path
# so that we import the correct version.py and finddata.py
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import version
from finddata import find_package_data


setup(name='arduino_helpers',
      version=version.getVersion(),
      description='Helper functions for reading configs, etc. from an '
      'installed Arduino directory.',
      author='Christian Fobel',
      author_email='christian@fobel.net',
      url='http://github.com/wheeler-microfluidics/arduino_helpers.git',
      license='GPLv2',
      install_requires=['serial_device', 'path_helpers'],
      packages=['arduino_helpers', 'arduino_helpers.hardware',
                'arduino_helpers.bin'],
      package_data=find_package_data())


@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass
