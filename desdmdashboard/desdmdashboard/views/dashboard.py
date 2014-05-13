import inspect

from django.shortcuts import render, render_to_response, get_object_or_404

from . import dashboard_figures


def entrance(request):
    '''
    '''

    all_functions = inspect.getmembers(dashboard_figures, inspect.isfunction)

    figures = {}
    for fs in all_functions:
        name, f = fs
        if f.__module__ == 'desdmdashboard.views.dashboard_figures':
            try:
                figstring = f()
                figures[' '.join(name.rsplit('_'))] = figstring
            except Exception, e:
                figures[' '.join(name.rsplit('_'))] = e

    return render_to_response('dashboard_main.html', {'figures': figures, }) 
