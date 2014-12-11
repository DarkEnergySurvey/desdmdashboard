
from monitor.models import Metric

from django.shortcuts import render, render_to_response, get_object_or_404


def get_vm_dict():
    vmmetrics = Metric.objects.filter(name__startswith='VM_')
    namelist = [vm['name'].rsplit('_')[1] for vm in vmmetrics.values('name')]
    vm_dict = { vm:vm.replace('.', '_') for vm in set(namelist)}
    return vm_dict


def get_vm_section_dict(vm):
    section_dicts = [ 'a', 'b', 'c', ]
    return section_dicts 
