#!/usr/bin/env python

from distutils.core import setup

setup(name='desdmdashboard',
      version='0.1.0',
      description='Web App for timeseries of snapshot data monitoring for DESDM.',
      author='Michael Graber',
      author_email='michael.graber@fhnw.ch',
      packages=[
          'desdmdashboard.monitor.feeddb',
#         'desdmreportingframework.templates',
#         'desdmreportingframework.utils',
          ],
#     package_dir = {'': 'packages'},
#     package_data = {
#         'css':['*.css'],
#         'desdmreportingframework': ['templates/jinja2/*.html'],
#         },
#     scripts=['bin/ReportingFW',]
     )

