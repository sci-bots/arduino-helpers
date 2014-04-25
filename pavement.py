import sys
from pprint import pprint

from paver.easy import task, needs, path
from paver.setuputils import setup

import version
# Add package directory to Python path. This enables the use of `arduino_helpers`
# functions for discovering, e.g., the path to the [AVR][1] tools.
#
# [1]: http://en.wikipedia.org/wiki/Atmel_AVR
sys.path.append(path('.').abspath())
import arduino_helpers

setup(name='arduino_helpers',
      version=version.getVersion(),
      description='Helper functions for reading configs, etc. from an '
      'installed Arduino directory.',
      author='Christian Fobel',
      author_email='christian@fobel.net',
      url='http://github.com/wheeler-microfluidics/arduino_helpers.git',
      license='GPLv2',
      packages=['arduino_helpers'])


@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass
