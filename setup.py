#!/usr/bin/env python

from setuptools import setup

setup(
name='fanout',
version='1.3.0',
description='Fanout.io library',
author='Justin Karneges',
author_email='justin@fanout.io',
url='https://github.com/fanout/pyfanout',
license='MIT',
py_modules=['fanout'],
install_requires=['pubcontrol>=2.2.0,<4'],
classifiers=[
	'Topic :: Utilities',
	'License :: OSI Approved :: MIT License'
]
)
