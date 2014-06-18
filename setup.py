#!/usr/bin/env python

from distutils.core import setup

setup(name='desdmdashboard',
      version='0.1.0',
      description=('Web App for timeseries of snapshot data monitoring for '
                    'DESDM. \nRemote components only!'),
      author='Michael Graber',
      author_email='michael.graber@fhnw.ch',
      packages=[
          'desdmdashboard_remote',
          'desdmdashboard_remote.senddata',
          'desdmdashboard_remote.receivedata',
          ],
     )
