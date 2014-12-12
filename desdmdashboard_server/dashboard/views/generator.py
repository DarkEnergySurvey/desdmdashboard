
import os
import re
import inspect

from docutils.core import publish_parts

from importlib import import_module

from django.shortcuts import render, render_to_response, get_object_or_404

from .. import models
from . import sections

from .sections.virtualmachines import get_vm_dict, get_vm_section_dict


EXCLUDE_FILENAME_REGEXPS = [
        '__init__.py',
        '.*.pyc$',
        'home.py',
        'virtualmachines.py', # treat separately
        ]

INCLUDE_FILENAME_REGEXP = '.*\.py$'


def dashboard_home(request):
    context = get_common_dashboard_context()
    home_module = import_module('dashboard.views.sections.home')
    section_dicts = get_module_function_outputs(home_module)
    context.update({
            'section_dicts': section_dicts,
            })
    return render_to_response('dashboard.html', context)


def dashboard_section(request, section=None):
    context = get_common_dashboard_context()
    section_modules = get_section_modules()
    section_dicts = get_module_function_outputs(section_modules[section])
    context.update({
            'section_name': section.replace('_', ' ').title(),
            'section_dicts': section_dicts,
            })
    return render_to_response('dashboard.html', context)


def virtualmachines(request, vm_slug=None):
    context = get_common_dashboard_context()
    context['section_name'] = 'virtualmachines'
    if vm_slug is None:
        context.update({ 'vmdict': get_vm_dict() })
    else:
        vm_name = vm_slug.replace('_', '.')
        section_dict = get_vm_section_dict(vm_name)
        context.update({
            'section_dicts': section_dict,
            'vm_name': vm_name,
            })

    return render_to_response('virtualmachines.html', context)


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


def get_section_modules():
    section_files = os.listdir(sections.__path__[0])
    section_modules = {}
    for sf in section_files:

        if any([re.match(ef, sf) for ef in EXCLUDE_FILENAME_REGEXPS]):
            continue
        if not re.match(INCLUDE_FILENAME_REGEXP, sf):
            continue

        module_name = sf.replace('.py', '')
        
        module = import_module('dashboard.views.sections.'+module_name)
        if not hasattr(module, 'ACTIVE'):
            section_modules[module_name] = import_module(
                    'dashboard.views.sections.'+module_name)
        elif module.ACTIVE == True:
            section_modules[module_name] = import_module(
                    'dashboard.views.sections.'+module_name)
        else:
            continue

    return section_modules


def get_common_dashboard_context():
    section_modules = get_section_modules()
    section_names = {s: s.replace('_', ' ').title() for s in
            section_modules.keys() }
    context = {
            'navsection': 'dashboard',
            'sections': section_names,
            'virtualmachines': get_vm_dict(), 
            }
    return context
