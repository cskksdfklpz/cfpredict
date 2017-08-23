#!/usr/bin/env python

def readme():
    with open('README.rst') as f:
        return f.read()

from setuptools import setup

setup(name='cfpredict',
      version='0.2',
      description='fine-grained prediction of commodity futures price',
      long_description=readme(),
      url='http://github.com/cskksdfklpz',
      author='Quanzhi Bi',
      author_email='cskksdfklpz@gmail.com',
      license='MIT',
      packages=['cfpredict'],
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points = {
        'console_scripts': ['info=cfpredict.command_line:main'],
     },
     install_requires=[
          'pandas',
          'numpy',
      ],
      zip_safe=False)
