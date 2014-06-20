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
`DESDMDashboard Remote`_ component and its dependencies (ipython, pandas,
CoreUtils). It allows you to send and receive data to and from the database
(see below) from any client machine via http requests.

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
view code. Each subsection (black menubar) is dynamically created by an
individual python file. However, tools that allow you to achieve that with only
a few lines of code are at hand. The **metric** section shows out of the box
information for each ``Metric`` measured, most importantly maybe about its
alert status.

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

A metric additionally has an ``owner``. It typically gets set automatically
through authentication but can be changed in the `Admin Interface`_, like the attributes mentioned above.


``MetricDataXYZ``` models have the following  attributes:

    -   ``value`` : the value measured in a native database format
    -   ``time`` : the timepoint of the measurement (is set automatically)
    -   ``has_error`` : measuring the metric led to an error
    -   ``error_message`` : can store the error_message originating from metric
        data measurement
    -   ``tags`` : you can label individual measurements with comma separated
        tags


REST web api
-------------------------------------------------------------------------------
The web application implements a REST web api that allows sending and receiving
data to and from the database. A browser web interface for the api can be found
in the **metric api** section.

The utilities in the `DESDMDashboard Remote`_ component make use of this api.


Admin Interface
-------------------------------------------------------------------------------
The DESDMDashboard web application comes with a customized django admin
interface which provides database access. It can be found in the **admin**
section.


Server Setup
-------------------------------------------------------------------------------
The desdmdashboard_server svn directory contains the code to run the django web
application on a server. An eups metapackage called **DASHBOARDSERVER**
contains all dependencies of the desdmdashboard_server code. The server machine
currently used is **desdash.cosmology.illinois.edu**. 

Server Configuration
''''''''''''''''''''
Resposible persons for the server setup and administration are Greg Daues and Michael Graber.



-------------------------------------------------------------------------------
DESDMDashboard Remote 
-------------------------------------------------------------------------------
When installing the **eups package desdmdashboard** (trunk+0) you get tools to
send and receive data via the web api of the desdmdashboard server application.
This provides you with the capability to send data from an arbitraty client
machine but also to inspect data stored on the server for investigation
purposes. The eups package contains third party tools to enable this process:
ipython (notebook), pandas, matplotlib, ..

While accessing the views on the DESDMDashboard website is open for everybody,
sending and receiving data through the web api requires authentication. The
package makes use of CoreUtils to automatically access your login credentials
for DESDMDashboard access. Therefore you need on your client machine a
``.desservices.ini`` file in your home directory. Add a section
``desdmdashboard`` as follows:

.. sourcecode:: ini
    
    [desdmdashboard]
    user = dito 
    passwd = dito
    api_url = http://desdash.cosmology.illinois.edu/dev/desdmdashboard/monitor/api

Please be aware that the ``api_url`` is correct for the currently developed
``/dev/`` version of DESDMDashboard only. As soon as we'll release a first
stable version of the dashboard, the ``api_url`` will need to be changed!

Sending Data
-------------------------------------------------------------------------------
If you are the owner of a given metric and would like to append data to its
data table or if you would like to create a new metric, you can do so by the
use of the ``senddata`` submodule. There are two different approaches to
sending data to the DESDMDashboard database:

First, you can use the straightforward function ``send_metric_value()``:

.. sourcecode:: python

    from desdmdashboard_remote.senddata.functions import send_metric_value

    send_metric_value('destest', 99)

Executing this code will send ``99`` to a metric called ``destest`` and write
the value in the corresponding ``MetricData`` table. In case said metric does
not exist yet **you have to declare the** ``value_type`` keyword argument:
``value_type`` can be ``int``, ``float``, ``char``, ``datetime`` or ``json``.
In the case of ``json`` the value argument has to be a valid json string, in
the case of ``datetime`` the api expects an isoformat datetime string, ie a
value of the form ``'YYYY-MM-DDTHH:mm:ss'``. Don't miss the ``T`` between the
date and the time ..

Furthermore, ``send_metric_value()`` accepts a number of keyword arguments: 
``tags``, ``has_error``, ``error_message``, ie basically all the attributes
that can be stored with an individual ``MetricData`` value. Thereby you get the
opportunity to partly relay data acquisition failure information.

Second, you can use a python function decoration:

.. sourcecode:: python

    from desdmdashboard_remote.senddata.decoraters import Monitor 

    @Monitor('destest')
    def this_function_measures_something():
        # your data gathering routine
        value = do_something()
        return value

Now, whenever ``this_function_measures_something()`` is executed, ``value`` is
automatically written into the DESDMDashboard database. You could use this
for example to declare a function in a python file that is supposed to be
executed as a script. You would then have to only add the function name into the
``if __name__ == '__main__':`` part, like:

.. sourcecode:: python

   # the above

   if __name__ == '__main__':
       this_function_measures_something()

A ``Profile()`` decorator is in development, but not fully ripe yet. It will
allow to decorate an arbitrary function. Function execution will then be
automatically profiled and the profiling information will be sent to the db.

The decorators take the same keyword arguments like the ``send_metric_value()``
function.

Receiving Data - Local Data Exploration
-------------------------------------------------------------------------------
Receiving data is intended to enable playing around on a local machine with the
datasets acquired. This can most powerfully be done by the use of third party
packages like pandas, matplotlib etc. Therefore these packages are dependencies
of the desdmdashboard eups package. Also, the functions provided return pandas
DataFrames right away:

.. sourcecode:: python

    from desdmdashboard_remote.receivedata.to_pandas import get_metric_dataframe, get_multimetric_dataframe 

    df1 = get_metric_dataframe('destest')

    df2 = get_multimetric_dataframe(
            (('metricA', 'owner_username'),
            ('metricB', 'owner_username'),
            ('metricC', 'owner_username'),),
            resample='D',
            )


Receiving data requires authentication as well, however you can read data from
arbitrary owners.

The desdmdashboard eups package
-------------------------------------------------------------------------------
Currently there is no tagged eups desdmdashboard package available yet, but
there is trunk package ready for use. It can be installed through eups using 

.. sourcecode:: bash

   -bash-$ eups distrib install desdmdashboard trunk+0



Using the IPython notenbook
-------------------------------------------------------------------------------

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



..  sourcecode:: bash

    $ blabla


