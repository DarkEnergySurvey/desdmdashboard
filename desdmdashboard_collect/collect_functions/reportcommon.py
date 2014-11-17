"""
Common utilites for reporting
"""
import sys
import time
import hashlib


def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print >> sys.stdout, '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper


#####################################
# SQL defining/using the query cache
#####################################
# detect if the query is alreay cached
CACHED_QUERY_DETECT_SQL="SELECT count(*)  FROM user_tables WHERE table_name = '%s'"

# create the cache index table, if not already created.
CACHE_CREATE_SQL="""DECLARE cnt NUMBER;
BEGIN
  SELECT count(*) INTO cnt FROM user_tables WHERE table_name = 'QCACHE_INDEX';
  IF cnt = 0 THEN
    EXECUTE IMMEDIATE 'CREATE TABLE  QCACHE_INDEX
        ( tablename varchar2(32) PRIMARY KEY,
          created DATE,
          expires DATE)
         ';
  END IF;
END; """

# register this query into the cache
CACHE_REGISTER_QUERY="""
MERGE INTO QCACHE_INDEX USING dual ON ( TABLENAME='%s' )
WHEN MATCHED THEN UPDATE SET CREATED = SYSDATE, EXPIRES = SYSDATE+%s
WHEN NOT MATCHED THEN INSERT (TABLENAME,CREATED,EXPIRES)
    VALUES ('%s', SYSDATE, SYSDATE+%s )
"""

# support purging expired entries -- get old tables, drop table, drop index entry
STALE_CACHE_TABLES_SQL = """select TABLENAME from QCACHE_INDEX where EXPIRES < SYSDATE"""
DROP_CACHE_TABLE_SQL = """DROP TABLE %s"""
DELETE_CACHE_INDEX_ROW_BY_TABLENAME =  """DELETE FROM QCACHE_INDEX where TABLENAME = '%s'"""
# support applications purging based on time since cache entry
NHOWOLDERTHAN="SELECT count(*) cnt FROM qcache_index WHERE tablename = '%s' AND created+%s < SYSDATE"
# (tablename, olderthan)

#  support purging the whole cache down
#  by returning all table names
ALL_CACHE_TABLE_SQL="""
    SELECT
      table_name
    FROM user_tables
    WHERE
      table_name
    LIKE
    'QCACHE_%'
"""

class Q(object):
   """ holds state for a query

       provide the programming elegance of returning
       an interable with tight notation, but provide
       a way to get query meta-data (like headers)

       class Q support program debug by suporting
       printing of queries and queries timing to
       stdout.

       The class method Q.query_via_cache passed
       queries thoug a cache kept in your mydb.
       a series of tables names QCACHE_ consititue
       the cache.  Queries are cahched for 4.0
       dats by default. The lifetime of newly
       created cache entries is 4.0 days.

       ** need to close the cursor! wrong semantics
   """
   def __init__(self, dbh, query, args):
      self.cur = dbh.cursor()
      self._header = None
      self.query=query
      self.args=args
      self.expire_days=4.0 #lifetime of data in cache in days

   def query_via_cache(self):
      """ dump query results into cache, return cursor to query"""
      if not self.args.use_query_cache:  #caching is a new and experimental feature
          return self._query(self.query, self.args)
      args=self.args
      query=self.query
      # make the cache table if it is not there
      self._query(CACHE_CREATE_SQL, args)
      #purge any old entries
      self.purge_stale_cache()
      #all queries are from the cache prepare the table name
      # and the eventual query)
      cached_table_name = self._table_name(query)
      cached_query = "SELECT * FROM %s" %  cached_table_name

      # is cached is the number of tables consistent with the hashed query name
      isCached=self._query(CACHED_QUERY_DETECT_SQL % cached_table_name, args).fetchall()[0][0]
      assert isCached < 2    #must be 0 or 1, ir the system is not sane
      if not isCached:
         # cache the query, then feed user from cache
         #  select into the cache
         #  register the query in the cache
         #  setup user service from the cache
         # get a unique table name
         query_prefix = "CREATE TABLE %s  AS " % cached_table_name
         cache_load_query = query_prefix + query
         # load the user's query into cache
         self._query(cache_load_query, args)
         # create a recod of the cached table.
         self._register_cache(cached_table_name, args)
         # now prepare query srring from cache into cache -- we'll query later)

      #execute cached_query and return the result to user
      cur = self._query(cached_query, args)
      return cur

   def _table_name(self, query):
      """ Produce a tablename to hold the cached query results """
      return "QCACHE_" + hashlib.sha224(query).hexdigest()[0:18].upper()

   def _register_cache(self, tablename, args):
      """ make entry for the queue in the QCAHE_INDEX table"""
      q = CACHE_REGISTER_QUERY  % (
         tablename, self.expire_days,tablename, self.expire_days)
      self._query(q, args)


   def _query(self, query, args):
      """ do query and return cursor print debug info when desired"""
      t0 = time.time()
      if args.debug : print >>sys.stderr, query
      self.cur.execute(query)
      if args.debug : print >>sys.stderr, "took %s seconds" % (time.time()-t0)
      if self.cur.description :
          #name, type, display_size, internal_size, precision, scale, null_ok
          self._header        = zip(*self.cur.description)[0]
          self._type          = zip(*self.cur.description)[1]
          self._display_size  = zip(*self.cur.description)[2]
          self._internal_size = zip(*self.cur.description)[3]
          self._precision     = zip(*self.cur.description)[4]
          self._scale         = zip(*self.cur.description)[5]
          self._null_ok       = zip(*self.cur.description)[6]
      return self.cur

   def q(self):
      """ perform query, return curssor, cahce header in case desired"""
      return self._query(self.query, self.args)

   def delete_cache(self):
      """ completely delete all your perosnal query cahce tables"""
      if not self.args.use_query_cache : return
      for table in self._query(ALL_CACHE_TABLE_SQL, self.args).fetchall():
         self._query("DROP TABLE %s" % table , self.args)

   def purge_stale_cache(self):
      """  remove all stale cache entries"""
      if not self.args.use_query_cache : return
      for table in self._query(STALE_CACHE_TABLES_SQL, self.args):
         self.purge_query(table)

   def purge_query(self, query, olderthan=0):
      """ remove a specific query from cache

          kwarg olderthan as a flat indicating the deletion is conditional
          on the chachced results being older than older than  days

           Oracle
           throws cx_Oracle.DatabaseError: ORA-00942: table or view does not exist
           we catch this, and silenelty succeed.
      """
      if not self.args.use_query_cache : return
      tablename = self._table_name(query)
      isOlder=self._query(NHOWOLDERTHAN % (tablename, olderthan), self.args).fetchall()[0][0]
      if not isOlder: return #def purge_query(self, query, olderthan=0): nothing to purge
      #rece condition protection
      try:
         self._query(DROP_CACHE_TABLE_SQL % tablename, self.args)
         self._query(DELETE_CACHE_INDEX_ROW_BY_TABLENAME % tablename, self.args)
      except cx_Oracle.DatabaseError:
         if 'ORA-00942' not in "%s" % sys.exc_info()[1] :
            raise

   def get_header(self):
      """ return list of column headers from the query """
      return [ h for h in self._header]


class  prettyPrinter(object):
   """
   print the data in columns of uniform width.

   the columns widths are automatically built
   use:
   prettyPrinter().pprint(data)

   defaultt formatting is used, and can be adjusted
   by setting type-specific formats. Ttwo API's exist
   formats can be anyting acceptable to
   format e.f {:f3.2} for float
   or a function rendering the type into a string.

   default formate are used for all types except for
   datetime deltatime and lists and tuples.

   """
   def __init__(self):
      import datetime
      self.fmatdict={}

      #default formats
      # datetimes --no usconds for datetimes (returned by Oracle, for example)
      self.set_format_by_type(datetime.datetime.today(), "{:%x %X}")


      #default functions are needed for more complesx type.
      #timedeltas -- no usecs and no days, just more than 24 hours for timedeltas
      # sets -- default is narrow, one set member and elipses  set has more than one...
      # lists, typle -- render according to primitive type, Join elements with comma
      td = lambda d : "{}:{}:{}".format(d.seconds/3600 + d.days*24,(d.seconds/60)%60,d.seconds%60)
      self.set_render_func_by_type(datetime.timedelta(1,1), td)
      self.set_render_func_by_type(set([1,2]), format_set)
      self.set_render_func_by_type([],self._render_list_to_string)
      self.set_render_func_by_type((),self._render_list_to_string)
      self.set_render_func_by_type({},self._render_dict_to_string)

   def set_format_by_type(self, value, format):
      """ set format for a types of which value is an instance
            e.g ps.et_format(type(1), '{:<5d}'

            iplemented by passinf the associated format function
            to the function variant of the...
       """
      self.set_render_func_by_type(value, format.format)
   def set_render_func_by_type(self, value, function):
       """ set a function that will render a type

           provides a function to format a thing of the given type
       """
       self.fmatdict[type(value)] = function
   def _render_thing(self, thing):
      """ return an ascii value based on type

           rendering turns a python variable into a string.
           using a format which can be specific to its type

      """
      function = "{:}".format
      if  self.fmatdict.has_key(type(thing)) :
         function  = self.fmatdict[type(thing)]
      return function(thing).strip()

   def _render(self, data):
      rendered=[]
      for row in data:
         rendered.append(self._render_row(row))
      return rendered


   def _render_row(self, alist):
      """ produce a list of ll the things in a list, rendered

          deta item that is itsells a list
          we want to amke sure we can render lists of dates
          acording to the format rules
      """
      return  [self._render_thing(item) for item in alist]

   def _width(self, array):
      """ return the width of the largest ascii element in  array"""
      return  max([len(self._render(c)) for c in array ])

   def _fmats(self, rdata):
      """ calculate the formats  to apply to  a row in the array

      This format is inteneded not to convert a type to ascii,
       but to blank pad an ascii type to produce a veritbal column
       """

      widths = [self._width(col) for col in zip(*rdata)]
      fmats = ' '.join(['{:>%d}' % width for width in widths ])
      return fmats

   def _assert(self, data):
      """
      ensure that data is per contract
      thsi has been a bug-abo in the pars

      -- all rowa are of equal length
      """
      lengths = [len(r) for r in data]
      least = min (lengths)
      most  = max (lengths)
      assert least == most

#############################################
#
#  Render complex types the user might present in
#  in a string.
#
#############################################

   def _render_list_to_string(self, alist):
      """
          render all the things in a 1-d list into a string
          used as the default renderer for a list type.


      """
      return  ",".join(self._render_row(alist))


   def _render_dict_to_string(self, adict):
      """
          render all the things in adictionary to a string.
      """
      alist = [ "%s:%s" % (self._render_thing(k),
                           self._render_thing(adict[k])
                           )  for k in adict.keys()]
      return  ",".join(self._render_row(alist))


   def pprint(self, data):
      """ prettytprint a 2-D array of uniform row lenght to sdtout"""
      self._assert(data)
      data = self._render(data)  # make elements ascii
      fmats = self._fmats(data)    # get array of padding formats)
      for row in data:
         print fmats.format(*row)

   def csvprint(self, data):
      """ write a CSV file to stdout"""
      import csv
      import sys
      # self._assert(data)  CSV data  row lenght can vary
      data = self._render(data)  # make elements ascii
      writer = csv.writer(sys.stdout, delimiter=',',
                          quotechar='"',
                          quoting=csv.QUOTE_MINIMAL,
                          lineterminator="\n")
      for row in data: writer.writerow(row)


########################################################
#
#  foratting support functions
#
########################################################

#
#  support for pretty printing sets.
#
def format_set_wide(set):
    formatSet(set, isWide=True)
def format_set(set, isWide=False):
    """render a set into a printable string

    if we are 'wide': then return a blank-seperated
    set elemements, if we are narrow return a
    member of the set, indicate that there  is more
    than one element of a set by appending elipsis...

    """
    if isWide:
        list = [s for s in set]
        ret = ";".join(list)
        return ret
    else:
        if len(set) == 0:
            return ""
        elif len(set) == 1:
            return "%s" % iter(set).next()
        else:
            return "%s..." % iter(set).next()


def create_run_str(reqnum, unitname, attnum):
    """ Create the standard string identifying a run to a human"""
    run = '%s_r%sp%02d' % (unitname, reqnum, int(attnum))
    return run

def unique_strings(l):
   dict = {}
   for s in l:
      dict[s] = 1
   return dict.keys()

def main(args):
   """ tests"""
   p = prettyPrinter()
   p.pprint ([
               ["xval", "yval"],
               [datetime.timedelta(1,12398) ,datetime.datetime.today()],
               [1.2, [1,2,3]],
               [set(["dog", "cat", "Dog"]), set(["dog"])],
               [ [ ["row1"],["row2a","row2b"]], {1:2, "dog":datetime.datetime.today()}]
             ])

   dbh = coreutils.DesDbi(os.path.join(os.getenv("HOME"),".desservices.ini"),args.section)
   sql="select SYSDATE d from DUAL"
   q=Q(dbh, sql, args)
   q.delete_cache()
   print "nest tewo results should be the same if cacheing"
   print q.query_via_cache().fetchall()
   time.sleep(2)
   q=Q(dbh, sql, args)
   print q.query_via_cache().fetchall()
   q.purge_query(sql)
   print "nest result should be different"
   time.sleep(2)
   q=Q(dbh, sql, args)
   print q.query_via_cache().fetchall()
   time.sleep(2)
   print "next result should be different"
   q.purge_query(sql, olderthan=0.0)
   q.purge_query("dog")  # invalid query
   print q.query_via_cache().fetchall()

if __name__ == "__main__":

   import os
   import sys
   import time
   import datetime
   import argparse
   import coreutils
   import cx_Oracle #needed to catch execptions

   """Create command line arguments"""
   parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
   parser.add_argument('--section','-s',default='db-desoper',
             help='section in the .desservices file w/ DB connection information')
   parser.add_argument('--debug','-d',help='print debug info', default=False, action='store_true')
   parser.add_argument('--header_off','-H',help='suppress header', default=False, action='store_true')
   parser.add_argument('--detailed','-D',help='report on every trasfer_batch', default=False, action='store_true')
   parser.add_argument('--wide','-w',help='be wide -- list all srouce, nodes, etc.', default=False, action='store_true')
   parser.add_argument('--csv','-c',help='print as a CSV (def pretty print)', default=False, action='store_true')
   parser.add_argument('--use_query_cache','-C',help='use the query cache feature', default=False, action='store_true')
   parser.add_argument('--days_back','-b',help='how far to got back in time(days)', default=1.0)

   args = parser.parse_args()

   main(args)
