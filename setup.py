#!/usr/bin/env python

from distutils.core import setup

setup(name='clearinghouseapi',
      version='1.0',
      description='Python SDK for FCC Clearinghouse APIs',
      author='Aaron Vimont',
      author_email='aaron.vimont@fcc.gov',
      packages=['clearinghouse', 'clearinghouse.tests']
     )