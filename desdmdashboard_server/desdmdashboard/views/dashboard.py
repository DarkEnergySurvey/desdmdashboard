import inspect
from docutils.core import publish_parts

from django.shortcuts import render, render_to_response, get_object_or_404

from . import dashboard_figures


def docu(request):
    '''
    '''
    
    docu_html = publish_parts(DOCU_STRING, writer_name='html', 
            settings_overrides={'doctitle_xform':False,
            'initial_header_level': 1,} )['html_body']
    context = { 'docu_content': docu_html }

    return render_to_response('dashboard_docu.html', context) 


DOCU_STRING = '''

===============================================================================
DESDMDashboard Documentation - v0.0.1
===============================================================================

DESDMDashboard is a tool for (timeseries) data monitoring. It provides
functionality to easily store snapshot measurements in a database, to display
them over time and to detect alert states.

DESDMDashboard consists of three components:
    -  `DESDMDashboard Server`_
    -  `DESDMDashboard Remote`_
    -  `DESDMDashboard Collect`_

They correspond with three directories in the desdmdashboard svn repository.

When installing the **desdmdashboard eups package** you install only the
desdmdasboard_remote part and its dependencies (ipython, pandas, CoreUtils). It
allows you to send and receive data to and from the database (see below).

In the first few sections of this documentation we are going to have a look at
the three components of the DESDMDashboard to clarify the concepts and terms
used. Thereafter we show in the Cookbook_ how to acquire new data, how to
display it on the dashboard etc.

-------------------------------------------------------------------------------
DESDMDashboard Server
-------------------------------------------------------------------------------

The desdmdashboard_server svn directory contains all the code to run the django
web application on a server. The server machine currently used is
**desdash.cosmology.illinois.edu**. An eups metapackage called
**DASHBOARDSERVER** contains all dependencies of the desdmdashboard_server
code.

Datamodel
-------------------------------------------------------------------------------
The underlaying datamodel for storing data consists of a table for metric meta
information called ``Metric`` and 5 tables for the storage of metric data in
native database formats: ``MetricDataInt``, ``MetricDataFloat``, ``MetricDataChar``,
``MetricDataDatetime``, ``MetricDataJSON``. Each ``Metric`` object needs to
declare a ``value_type`` defining in which data table associated data is going
to be written.

    -   Monitor / Metric Data Model
    -   web api
    -   api
    -   admin

..  sourcecode:: bash

    $ blabla



-------------------------------------------------------------------------------
DESDMDashboard Remote 
-------------------------------------------------------------------------------
When installing the **eups package desdmdashboard** (trunk+0) you get tools to
send and receive data via the web api of the desdmdashboard server application.
This provides you with the opportunity to send data from arbitraty client
machine but also to inspect data stored on the server for investigation
purposes on any machine. The eups package contains third party tools to enable
this process: ipython (notebook), pandas, matplotlib, ..

    -   sending and receiving data
    -   installing the desdmdashboard eups package
    -   starting an ipython notenbook
    -   receiving data from the database
    -   sending data to the database


-------------------------------------------------------------------------------
DESDMDashboard Collect
-------------------------------------------------------------------------------
    -   data collection in principal
    -   cron jobs on desdash
    -   the cronjob log
    -   setting up new collection jobs 


-------------------------------------------------------------------------------
Cookbook
-------------------------------------------------------------------------------

.. sourcecode:: python

    from desdmdashboard_remote.senddata.functions import send_metric_to_database

    send_metric_to_database('destest', 99)

blablabla


'''

"""
    The Pygments reStructuredText directive
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This fragment is a Docutils_ 0.5 directive that renders source code
    (to HTML only, currently) via Pygments.

    To use it, adjust the options below and copy the code into a module
    that you import on initialization.  The code then automatically
    registers a ``sourcecode`` directive that you can use instead of
    normal code blocks like this::

        .. sourcecode:: python

            My code goes here.

    If you want to have different code styles, e.g. one with line numbers
    and one without, add formatters with their names in the VARIANTS dict
    below.  You can invoke them instead of the DEFAULT one by using a
    directive option::

        .. sourcecode:: python
            :linenos:

            My code goes here.

    Look at the `directive documentation`_ to get all the gory details.

    .. _Docutils: http://docutils.sf.net/
    .. _directive documentation:
       http://docutils.sourceforge.net/docs/howto/rst-directives.html

    :copyright: Copyright 2006-2014 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

# Options
# ~~~~~~~

# Set to True if you want inline CSS styles instead of classes
INLINESTYLES = False

from pygments.formatters import HtmlFormatter

# The default formatter
DEFAULT = HtmlFormatter(noclasses=INLINESTYLES)

# Add name -> formatter pairs for every variant you want to use
VARIANTS = {
    # 'linenos': HtmlFormatter(noclasses=INLINESTYLES, linenos=True),
}


from docutils import nodes
from docutils.parsers.rst import directives, Directive

from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer

class Pygments(Directive):
    """ Source code syntax hightlighting.
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = dict([(key, directives.flag) for key in VARIANTS])
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()
        # take an arbitrary option if more than one is given
        formatter = self.options and VARIANTS[list(self.options)[0]] or DEFAULT
        parsed = highlight(u'\n'.join(self.content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]

directives.register_directive('sourcecode', Pygments)
