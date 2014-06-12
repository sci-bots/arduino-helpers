from paver.easy import task, needs
from paver.setuputils import setup

import version


setup(name='arduino_helpers',
      version=version.getVersion(),
      description='Helper functions for reading configs, etc. from an '
      'installed Arduino directory.',
      author='Christian Fobel',
      author_email='christian@fobel.net',
      url='http://github.com/wheeler-microfluidics/arduino_helpers.git',
      license='GPLv2',
      install_requires=['serial_device'],
      packages=['arduino_helpers'])


@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass
