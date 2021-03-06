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

The DESDMDashboard website
-------------------------------------------------------------------------------
The web application consists of five different sections that are listed in the
navigation menu on the top right of the website. The **dashboard** is supposed
to display summary and overview plots and/or tables for *multiple metrics*. The
dashboard is generated by individual python view files that can be found in
``desdmdashboard_server/dashboard/views/sections/`` in the desdmdashboard svn
repository. Each file automatically creates a menu item in the black menu bar.
The dashboard summary data displays have to be implemented individually,
however, tools that allow you to achieve that with only a few lines of code are
at hand.

The **metrics** section shows out of the box information for each ``Metric``
measured, most importantly maybe about its alert status.

REST api
```````````````````````````````````````````````````````````````````````````````
The web application implements a REST web api that allows sending and receiving
data to and from the database. A browser web interface for the api can be found
in the **metric api** section.

The utilities in the `DESDMDashboard Remote`_ component make use of this api.


Admin Interface
```````````````````````````````````````````````````````````````````````````````
The DESDMDashboard web application comes with a customized django admin
interface which provides database access. It can be found in the **admin**
section.


Data model
-------------------------------------------------------------------------------
The underlaying data model for storing data consists of a table for metric meta
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
    -   ``expression_string``: a string that is evaluated by using the ``eval``
        statement. You can access the entire timeseries dataset in a pandas
        dataframe with name ``data`` within the evaluation string. The ``eval``
        statement output can currently only be inspected in the admin
        interface.

A metric additionally has an ``owner``. It typically gets set automatically
through authentication but can be changed in the `Admin Interface`_, like the
attributes mentioned above.


``MetricDataXYZ``` models have the following  attributes:

    -   ``value`` : the value measured in a native database format
    -   ``time`` : the timepoint of the measurement (is set automatically)
    -   ``has_error`` : measuring the metric led to an error
    -   ``error_message`` : can store the error_message originating from metric
        data measurement
    -   ``tags`` : you can label individual measurements with comma separated
        tags

Server Setup
-------------------------------------------------------------------------------
The desdmdashboard_server svn directory contains the code to run the django web
application on a server. An eups metapackage called **DASHBOARDSERVER**
contains all dependencies of the desdmdashboard_server code. The server machine
currently used is **desdash.cosmology.illinois.edu**. 

Server Configuration
```````````````````````````````````````````````````````````````````````````````
Resposible persons for the server setup and administration are Greg Daues and Michael Graber.



-------------------------------------------------------------------------------
DESDMDashboard Remote 
-------------------------------------------------------------------------------
When installing the **eups package desdmdashboard** (trunk+0) you get tools to
send and receive data via the web api of the desdmdashboard server application.
This provides you with the capability to send data from an arbitraty client
machine but also to receive and inspect data stored on the server on a local
machine. The eups package contains third party tools to enable this process:
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

    send_metric_value('test', 99)

Executing this code will send ``99`` to a metric called ``test`` and write
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

    @Monitor('test', value_type='int')
    def this_function_measures_something():
        # your data gathering routine
        value = do_something()
        return value

Now, whenever ``this_function_measures_something()`` is executed, ``value`` is
automatically written into the DESDMDashboard database in the data table of a
metric called ``test``. You could use this for example to declare a function
in a python file that is supposed to be executed as a script. You would then
have to only add the function name into the ``if __name__ == '__main__':``
part, like:

.. sourcecode:: python

   # the above

   if __name__ == '__main__':
       this_function_measures_something()

In case your measurement function takes arguments and you would like that these
arguments can also parametrize your metric name you can define a function
``generate_metric_name_xyz`` that takes the same arguments as your measurement
function and returns a string. You can then replace the name string in the
decoration with the name generating function:

.. sourcecode:: python

    def generate_metric_name_something(arg1, arg2):
        name = 'something_{a1}_{a2}'
        return name.format(a1=arg1, a2=arg2)

    @Monitor(generate_metric_name_something, value_type='int')
    def this_function_measures_something(arg1, arg2):
        # your data gathering routine
        value = do_something()
        return value

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

    df1 = get_metric_dataframe('test')

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
there is a trunk package ready for use. It can be installed through eups using 

.. sourcecode:: bash

   -bash-$ eups distrib install desdmdashboard trunk+0

The desdmdashboard eups package comes with the dependencies

    -   pandas
    -   ipython
    -   CoreUtils

and of course the eups dependencies (e.g. matplotlib) of these packages.

After installation use

.. sourcecode:: bash

   -bash-$ setup desdmdashboard trunk+0

to make the packages available on your machine.


Using the IPython notebook
-------------------------------------------------------------------------------
A powerful way to play around with your data is in the setting of an `IPython
<http://www.ipython.org>`_ notebook. An IPython notebook server can be run on
your local machine using

.. sourcecode:: bash

   -bash-$ ipython notebook 

Find documentation about IPython notebooks on the website of the IPython
project.

Since the ``receivedata.to_pandas`` functions return pandas DataFrames having a
look at the `pandas <http://pandas.pydata.org>`_ docu pages might be helpful.


-------------------------------------------------------------------------------
DESDMDashboard Collect
-------------------------------------------------------------------------------
Data collection is possible from any machine that can place http-requests to
the desdmdashboard web api. To bundle data collection tasks we provide the
**DESDMDashboard collect** package. The package consists of three subpackages:

    -   ``collect_utils``
    -   ``collect_functions``
    -   ``collect_jobs``

In the ``collect_utils`` we provide general utilities, for example for database
access etc, that support data collection. The proper functions that are
executed when a metric measurement is done are supposed to be found in
``collect_functions``. ``collect_jobs`` contains python scripts that are
started as ``cron jobs`` with a give frequency and therefore mainly contain
function calls of ``collect_functions``-functions.

As a convention we name the files that are to be executed on a particular
machine in the case of the ``collect_jobs`` scripts with
``machinename_x_hourly_optionaldescription.py``. In the case of the
``collect_functions`` the naming is analogous if the function is bound to a
machine: ``machinename_description.py``. 

The ``collect_jobs`` can be run in the correct eups environment by using the
bash script ``collect_cron_job``:

.. sourcecode:: bash
    
   -bash-$ path/to/collect_cron_job path/to/config/collect_cron_job__xyz.cfg path/to/collect_jobs/xyz_x_hourly.py

The first argument to the ``collect_cron_job`` script is the configuration file
the second argument is the job file. The template configuration file provided
in the svn repository currently looks as follows:

.. sourcecode:: config

    #!/bin/bash

    ###############################################################
    # Configuration file for DESDMDashboard data collection jobs.
    ###############################################################

    # THE DIRECTORY WHERE THE EUPS INSTALLATION RESIDES
    export EUPS_HOME="$HOME/eups"

    # CODE PATH
    export DESDMDASHBOARD_CODE_PATH="$HOME/desdmdashboard/trunk"

    # LOG CONFIGURATION 
    export COLLECT_LOG_DIR=$HOME
    export COLLECT_LOG_FILE='desdmdashboard_collect.log'


To excute the scripts in a cronjob edit the ``crontab`` file

.. sourcecode:: bash
    
   -bash-$ crontab -e
    
using the crontab job declaration scheme:

.. sourcecode:: cron

     +---------------- minute (0 - 59)
     |  +------------- hour (0 - 23)
     |  |  +---------- day of month (1 - 31)
     |  |  |  +------- month (1 - 12)
     |  |  |  |  +---- day of week (0 - 6) (Sunday=0 or 7)
     |  |  |  |  |
     +  *  *  *  *  command to be executed

For data collection jobs that do not rely on being executed on a specific
machine we suggest a centralized copy of the svn repository on the **desdash**
VM. The **DESDMDashboard collect** code can be found on desdash in
``/desdmdashboard_collect``. 


Logging
-------------------------------------------------------------------------------
You can append to a common log file from an arbitrary file or function that is run using
the same configuration file through the ``collect_cron_job`` script as
specified above by the use of a common logger:

.. sourcecode:: python

    from collect_utils import log
    logger = log.get_logger('desdmdashboard_collect')

    logger.info('My general info.')
    logger.debug('My debug info.')
    logger.error('My error statement.')

-------------------------------------------------------------------------------
Cookbook
-------------------------------------------------------------------------------

In this section we briefly present how to get a new dataset being displayed on
the DESDMDashboard website.


1. Collect metric data
-------------------------------------------------------------------------------
Define the content of the metric you would like to measure and implement a
python script that produces an individual measurement and sends it to the
DESDMDashboard website by the use of one of the two methods mentioned above.
Does your function have to be executed on a particular machine? If not add it
to the ``desdmdashboard_collect`` package in ``collect_functions`` and set up
``cronjob`` that executes your function with the desired frequency.
For example in the case of the file archive stats:

.. sourcecode:: python

    from desdmdashboard_remote.senddata.functions import send_metric_value 
    from collect_utils.database import make_db_query

    from collect_utils import log 
    logger = log.get_logger('desdmdashboard_collect')

    def file_archive_info__sum_filesize__archive_name():
        '''
        '''
        logger.info('file_archive_info__sum_filesize__archive_name entered.')

        QUERY = '''
            SELECT archive_name, SUM(filesize)
            FROM file_archive_info
            GROUP BY archive_name
            '''

        logger.info('executing db query')
        try:
            records = make_db_query(QUERY, section='db-destest')
            logger.info('db query successfully executed.')
        except:
            logger.error('db query not successfull.')
        return

        for record in records:

            archive_name = record[0]
            archive_size = record[1]

            metric_name = 'size '+archive_name

            logger.info('sending value for metric %s to db' % metric_name)
            req = send_metric_value(metric_name, archive_size, value_type='int')
            if req.error_status[0]:
                logger.error(req.error_status[1])


This is the corresponding ``collect_jobs`` file ``4_hourly.py``:

.. sourcecode:: python

    from collect_utils import log 
    logger = log.get_logger('desdmdashboard_collect')


    from collect_functions.destest import file_archive_info__sum_filesize__archive_name


    def main():
        file_archive_info__sum_filesize__archive_name()
    

    if __name__ == '__main__':
        logger.info('Start 4 hourly data collection script.')
        main()
        logger.info('4 hourly data collection script finished.')


Then edit the ``crontab`` as described above.

After you started collecting data you should right away see the metric
appearing in the *metrics* section of the website.

2. Add metric meta information in the admin 
-------------------------------------------------------------------------------
In case you would like to detect threshold crossings of some kind you can edit
the attributes of your metric in the **admin** interface. Please also add
**metric documentation** if you can provide any. **Especially if your metric
data is generated on a remote machine**. You can even add the code to the
``doc`` text field to make it transparent how your data is generated. The doc field is displayed in the metric detail view ..

3. Add a custom view to the dashboard
-------------------------------------------------------------------------------
In case the standard metric view in the metrics section is not enough for you
or your would like to create a summary view of multiple metrics, you have to
edit the dashboard code in the DESDMDashboard Server package.

The summary plot for the file archive stats is generated by the following code
that can be found in
``desdmdashboard_server/dashboard/views/sections/file_archive.py``:

.. sourcecode:: python

   from monitor import pandas_utils
   from dashboard.views.plotutils import plot_df_to_svg_string

   def size():
       '''
       '''
       df = pandas_utils.get_multimetric_dataframe(
               (('size desar2home', 'mgraber',),),
               resample='D',
               )
       figstring = plot_df_to_svg_string(df, style='.-', logy=True)
       return figstring


-------------------------------------------------------------------------------
Feedback ..
-------------------------------------------------------------------------------
\.. about this documentation or the DESDMDashboard in general is welcome
and should be directed to `Michael Graber <michael.graber@fhnw.ch>`_.
