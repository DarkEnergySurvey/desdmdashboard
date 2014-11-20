
import os
import re
import inspect

from docutils.core import publish_parts

from importlib import import_module

from django.shortcuts import render, render_to_response, get_object_or_404

from .. import models
from . import sections


EXCLUDE_FILENAME_REGEXPS = [
        '__init__.py',
        '.*.pyc$',
        'home.py',
        ]

INCLUDE_FILENAME_REGEXP = '.*\.py$'


def get_section_modules():
    section_files = os.listdir(sections.__path__[0])
    section_modules = {}
    for sf in section_files:

        if any([re.match(ef, sf) for ef in EXCLUDE_FILENAME_REGEXPS]):
            continue
        if not re.match(INCLUDE_FILENAME_REGEXP, sf):
            continue

        module_name = sf.replace('.py', '')
        section_modules[module_name] = import_module(
                'dashboard.views.sections.'+module_name)
    return section_modules


def dashboard_home(request):
    section_modules = get_section_modules()
    home_module = import_module('dashboard.views.sections.home')
    section_dicts = get_module_function_outputs(home_module)
    section_names = {s: s.replace('_', ' ').title() for s in
            section_modules.keys() }
    context = {
            'navsection': 'dashboard',
            'sections': section_names,
            'section_dicts': section_dicts,
            }
    return render_to_response('dashboard.html', context)


def dashboard_section(request, section=None):
    section_modules = get_section_modules()
    section_dicts = get_module_function_outputs(section_modules[section])
    section_names = {s: s.replace('_', ' ').title() for s in
            section_modules.keys() }
    context = {
            'navsection': 'dashboard',
            'sections': section_names,
            'section_name': section.replace('_', ' ').title(),
            'section_dicts': section_dicts,
            }
    return render_to_response('dashboard.html', context)


def get_module_function_outputs(module):
    all_functions = inspect.getmembers(module, inspect.isfunction)
    outputs = {}
    for fs in all_functions:
        name, f = fs
        if f.__module__ == module.__name__:
            try:
                sectiondict = f()
                if f.__doc__:
                    doc_html = publish_parts(f.__doc__, writer_name='html',
                            settings_overrides={
                                'doctitle_xform':False,
                                'initial_header_level': 4,
                                'report_level': 'quiet'}
                            )['html_body']
                    sectiondict['doc'] = doc_html
                outputs[' '.join(name.rsplit('_')).title()] = sectiondict
            except Exception, e:
                outputs[' '.join(name.rsplit('_')).title()] = e
            
    return outputs
