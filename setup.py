#!/usr/bin/env python3

from distutils.core import setup

from os.path import isdir, isfile
from setuptools import find_packages
from sys import argv

with open('README', 'r') as f:
    long_description = f.read()

version = 'unknown'
if isdir('.git'):
    try:
        from gitversionbuilder.main import get_version
        version = get_version('.').version_string

        with open('VERSION', 'w') as f:
            f.write(version)
    except Exception as e:
        print(str(e))
elif isfile('VERSION'):
    with open('VERSION', 'r') as f:
        version = f.read()


install_requires = [
    'PyGithub>=1.32',
]
setup_requires = [
    'pytest-runner>=2.9',
]
tests_require = [
    'mypy>=0.501',
    'pytest>=3.0.0',
    'pytest-catchlog>=1.2.0',
    'pytest-cov>=2.4.0'
]

# set min requires
if '--requires-min' in argv:
    argv.remove('--requires-min')
    install_requires = [require.replace('>=', '==') for require in install_requires]
    setup_requires = [require.replace('>=', '==') for require in setup_requires]
    tests_require = [require.replace('>=', '==') for require in tests_require]

setup(name='htwg-syslab-reviewer',
      version=version,
      description='HTWG syslab reviewer',
      long_description=long_description,
      license='MIT',
      author='Simon Wörner',
      author_email='htwg@simon-woerner.de',
      packages=find_packages(exclude=['tests', 'tests.*']),
      # package_data={'otm.helper': ['config_schema.yml']},
      # data_files=[('/etc/otm', ['config/otm-importer.sample.yml', 'config/logging.sample.ini'])],
      entry_points={
          'console_scripts': [
              'syslab-reviewer = htwg.syslab.reviewer.main:main',
          ],
      },
      install_requires=install_requires,
      setup_requires=setup_requires,
      tests_require=tests_require,
      )
