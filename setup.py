#!/usr/bin/env python

from setuptools import setup

setup(
name='fanout',
version='1.1.1',
description='Fanout.io library',
author='Justin Karneges',
author_email='justin@fanout.io',
url='https://github.com/fanout/pyfanout',
license='MIT',
py_modules=['fanout'],
install_requires=['pubcontrol>=2.1.1,<3'],
classifiers=[
	'Topic :: Utilities',
	'License :: OSI Approved :: MIT License'
]
)
