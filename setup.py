#!/usr/bin/env python

def readme():
    with open('README.rst') as f:
        return f.read()

from setuptools import setup

setup(name='cfpredict',
      version='0.1',
      description='fine-grained prediction of commodity futures price',
      long_description=readme(),
      url='http://github.com/cskksdfklpz',
      author='Quanzhi Bi',
      author_email='cskksdfklpz@gmail.com',
      license='MIT',
      packages=['cfpredict'],
      zip_safe=False)
