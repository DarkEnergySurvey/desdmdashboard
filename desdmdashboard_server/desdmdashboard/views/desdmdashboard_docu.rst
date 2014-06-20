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
allows you to send and receive data to and from the database (see below) from
any client machine via http requests.

In the first few sections of this documentation we are going to have a look at
the three components of the DESDMDashboard to clarify the concepts and terms
used. Thereafter we show in the Cookbook_ how to acquire new data, how to
display it on the dashboard etc.

-------------------------------------------------------------------------------
DESDMDashboard Server
-------------------------------------------------------------------------------
The central unit of the DESDMDashboard is its web application. It is
implemented using the `django <http://www.djangoproject.com>`_ python web
framework.

The web application provides the possibility to put on views of summary data
displays that consist of multiple metrics in the **dashboard** section. These
summary data displays have to implemented individually as part of the web app
view code. However, tools that allow you to achieve that with only a few lines
of code are at hand. The **metric** section shows out of the box information
for each ``Metric`` measured.

Datamodel
-------------------------------------------------------------------------------
The underlaying datamodel for storing data consists of a table for metric meta
information called ``Metric`` and 5 tables for the storage of metric data in
native database formats: ``MetricDataInt``, ``MetricDataFloat``, ``MetricDataChar``,
``MetricDataDatetime``, ``MetricDataJSON``. Each ``Metric`` object needs to
declare a ``value_type`` defining in which data table associated data is going
to be written.

Furthermore the ``Metric`` model allows you to set 

    -   ``warning_if_no_value_after_seconds`` : set this value to detect data
        source staleness
    -   ``show_on_dashboard`` : flag ``False`` if you do
        not want it to be displayed
    -   ``unit``
    -   ``alert_value``
    -   ``alert_operator`` : the operator used to compare the ``alert_value``
    -   ``doc`` : some documentation text

``MetricDataXYZ``` models 


REST web api
-------------------------------------------------------------------------------
The web application implements a REST web api.



Admin Interface
-------------------------------------------------------------------------------
Django provides an almost ready to use web interface to the database. It can be
customized in ``admin.py`` files for every django webapp.


Server Setup
-------------------------------------------------------------------------------
The desdmdashboard_server svn directory contains the code to run the django web
application on a server. An eups metapackage called **DASHBOARDSERVER**
contains all dependencies of the desdmdashboard_server code. The server machine
currently used is **desdash.cosmology.illinois.edu**. 

Server Configuration
''''''''''''''''''''


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


