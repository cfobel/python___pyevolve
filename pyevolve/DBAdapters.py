"""
:mod:`DBAdapters` -- database adapters for statistics
=====================================================================

.. warning:: the use the of a DB Adapter can reduce the performance of the
             Genetic Algorithm.

Pyevolve have a feature in which you can save the statistics of every
generation in a database, file or call an URL with the statistics as param.
You can use the database to plot evolution statistics graphs later. In this
module, you'll find the adapters above cited.

.. seealso::

   Method :meth:`GSimpleGA.GSimpleGA.setDBAdapter`
      DB Adapters are set in the GSimpleGA Class.

"""

import Consts
import Util
import sqlite3
import logging
import types
import datetime
import Statistics
import urllib
import csv
import xmlrpclib

class DBBaseAdapter:
   """ DBBaseAdapter Class - The base class for all DB Adapters
   
   If you want to create your own DB Adapter, you must subclass this
   class.

   :param frequency: the the generational dump frequency

   .. versionadded:: 0.6
      Added the :class:`DBBaseAdapter` class.
   """
   def __init__(self, frequency, identify):
      """ The class constructor """
      self.statsGenFreq = frequency

      if identify is None:
         self.identify = datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%y-%H:%M")
      else:
         self.identify = identify

   def setIdentify(self, identify):
      """ Sets the identify of the statistics
      
      :param identify: the id string
      """
      if identify is None:
         self.identify = datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%y-%H:%M")
      else:
         self.identify = identify

   def getIdentify(self):
      """ Return the statistics identify
      
      :rtype: identify string
      """
      return self.identify

   def getStatsGenFreq(self):
      """ Returns the frequency of statistical dump
      
      :rtype: the generation interval of statistical dump
      """
      return self.statsGenFreq

   def setStatsGenFreq(self, statsGenFreq):
      """ Set the frequency of statistical dump
      
      :param statsGenFreq: the generation interval of statistical dump
      """
      self.statsGenFreq = statsGenFreq

   def open(self):
      """ This method is called one time to do the initialization of
      the DB Adapter """
      pass

   def commitAndClose(self):
      """ This method is called at the end of the evolution, to closes the
      DB Adapter and commit the changes """
      pass

   def insert(self, stats, population, generation):
      """ Insert the stats

      :param stats: statistics object (:class:`Statistics.Statistics`)
      :param population: population to insert stats (:class:`GPopulation.GPopulation`)
      :param generation: the generation of the insert
      """
      Util.raiseException("This method is not implemented on the ABC", NotImplementedError)

class DBFileCSV(DBBaseAdapter):
   """ DBFileCSV Class - Adapter to dump statistics in CSV format

   Example:
      >>> adapter = DBFileCSV(filename="file.csv", identify="run_01",
                              frequency = 1, reset = True)

      :param filename: the CSV filename
      :param identify: the identify of the run
      :param frequency: the generational dump frequency
      :param reset: if is True, the file old data will be overwrite with the new

   .. versionadded:: 0.6
      Removed the stub methods and subclassed the :class:`DBBaseAdapter` class.

   """
   def __init__(self, filename=Consts.CDefCSVFileName, identify=None,
                frequency = Consts.CDefCSVFileStatsGenFreq, reset=True):
      """ The creator of DBFileCSV Class """

      DBBaseAdapter.__init__(self, frequency, identify)
      
      self.filename = filename
      self.csvWriter = None
      self.fHandle = None
      self.reset = reset

   def __repr__(self):
      """ The string representation of adapter """
      ret = "DBFileCSV DB Adapter [File='%s', identify='%s']" % (self.filename, self.getIdentify())
      return ret

   def open(self):
      """ Open the CSV file or creates a new file """
      logging.debug("Opening the CSV file to dump statistics [%s]", self.filename)
      if self.reset: open_mode = "w"
      else: open_mode = "a"
      self.fHandle = open(self.filename, open_mode)
      self.csvWriter = csv.writer(self.fHandle, delimiter=';')

   def close(self):
      """ Closes the CSV file handle """
      logging.debug("Closing the CSV file [%s]", self.filename)
      if self.fHandle:
         self.fHandle.close()

   def commitAndClose(self):
      """ Commits and closes """
      self.close()

   def insert(self, stats, population, generation):
      """ Inserts the stats into the CSV file

      :param stats: statistics object (:class:`Statistics.Statistics`)
      :param population: population to insert stats (:class:`GPopulation.GPopulation`)
      :param generation: the generation of the insert

      """
      line = [self.getIdentify(), generation]
      line.extend(stats.asTuple())
      self.csvWriter.writerow(line)

class DBURLPost(DBBaseAdapter):
   """ DBURLPost Class - Adapter to call an URL with statistics

   Example:
      >>> dbadapter = DBSQLite(url="http://localhost/post.py", identify="test")


   The parameters that will be sent is all the statistics described in the :class:`Statistics.Statistics`
   class, and the parameters:
   
   **generation**
      The generation of the statistics

   **identify**
      The id specified by user

   .. note:: see the :class:`Statistics.Statistics` documentation.

   :param url: the URL to be used
   :param identify: the identify of the run
   :param frequency: the generational dump frequency
   :param post: if True, the POST method will be used, otherwise GET will be used.

   .. versionadded:: 0.6
      Removed the stub methods and subclassed the :class:`DBBaseAdapter` class.
   """
   
   def __init__(self, url, identify=None,
                frequency = Consts.CDefURLPostStatsGenFreq, post=True):
      """ The creator of the DBURLPost Class. """

      DBBaseAdapter.__init__(self, frequency, identify)

      self.url = url
      self.post = post

   def __repr__(self):
      """ The string representation of adapter """
      ret = "DBURLPost DB Adapter [URL='%s', identify='%s']" % (self.url, self.getIdentify())
      return ret

   def insert(self, stats, population, generation):
      """ Sends the data to the URL using POST or GET
   
      :param stats: statistics object (:class:`Statistics.Statistics`)
      :param population: population to insert stats (:class:`GPopulation.GPopulation`)
      :param generation: the generation of the insert

      """
      logging.debug("Sending http request to %s.", self.url)
      response = None
      params = stats.internalDict.copy()
      params["generation"] = generation
      params["identify"] = self.getIdentify()
      if self.post: # POST
         response = urllib.urlopen(self.url, urllib.urlencode(params))
      else: # GET
         response = urllib.urlopen(self.url + "?%s" % (urllib.urlencode(params)))
      if response: response.close()

class DBSQLite(DBBaseAdapter):
   """ DBSQLite Class - Adapter to dump data in SQLite3 database format
   
   Example:
      >>> dbadapter = DBSQLite(identify="test")

   When you run some GA for the first time, you need to create the database, for this, you
   must use the *resetDB* parameter:

      >>> dbadapter = DBSQLite(identify="test", resetDB=True)

   This parameter will erase all the database tables and will create the new ones.
   The *resetDB* parameter is different from the *resetIdentify* parameter, the *resetIdentify*
   only erases the rows with the same "identify" name.   

   :param dbname: the database filename
   :param identify: the identify if the run
   :param resetDB: if True, the database structure will be recreated
   :param resetIdentify: if True, the identify with the same name will be overwrite with new data
   :param frequency: the generational dump frequency
   :param commit_freq: the commit frequency

   """

   def __init__(self, dbname=Consts.CDefSQLiteDBName, identify=None, resetDB=False,
                resetIdentify=True, frequency=Consts.CDefSQLiteStatsGenFreq,
                commit_freq=Consts.CDefSQLiteStatsCommitFreq):
      """ The creator of the DBSQLite Class """

      DBBaseAdapter.__init__(self, frequency, identify)

      self.connection = None
      self.resetDB = resetDB
      self.resetIdentify = resetIdentify
      self.dbName = dbname
      self.typeDict = { types.FloatType : "real" }
      self.cursorPool = None
      self.commitFreq = commit_freq

   def __repr__(self):
      """ The string representation of adapter """
      ret = "DBSQLite DB Adapter [File='%s', identify='%s']" % (self.dbName, self.getIdentify())
      return ret

   def open(self):
      """ Open the database connection """
      logging.debug("Opening database, dbname=%s", self.dbName)
      self.connection = sqlite3.connect(self.dbName)

      temp_stats = Statistics.Statistics()
      self.createStructure(temp_stats)

      if self.resetDB:
         self.resetStructure(Statistics.Statistics())

      if self.resetIdentify:
         self.resetTableIdentify()
   
   def commitAndClose(self):
      """ Commit changes on database and closes connection """
      self.commit()
      self.close()

   def close(self):
      """ Close the database connection """
      logging.debug("Closing database.")
      if self.cursorPool:
         self.cursorPool.close()
         self.cursorPool = None
      self.connection.close()

   def commit(self):
      """ Commit changes to database """
      logging.debug("Commiting changes to database.")
      self.connection.commit()

   def getCursor(self):
      """ Return a cursor from the pool

      :rtype: the cursor

      """
      if not self.cursorPool:
         logging.debug("Creating new cursor for database...")
         self.cursorPool = self.connection.cursor()
         return self.cursorPool
      else:
         return self.cursorPool

   def createStructure(self, stats):
      """ Create table using the Statistics class structure

      :param stats: the statistics object

      """
      c = self.getCursor()
      pstmt = "create table if not exists %s(identify text, generation integer, " % (Consts.CDefSQLiteDBTable)
      for k, v in stats.items():
         pstmt += "%s %s, " % (k, self.typeDict[type(v)])
      pstmt = pstmt[:-2] + ")"
      logging.debug("Creating table %s: %s.", Consts.CDefSQLiteDBTable, pstmt)
      c.execute(pstmt)

      pstmt = """create table if not exists %s(identify text, generation integer,
              individual integer, fitness real, raw real)""" % (Consts.CDefSQLiteDBTablePop)
      logging.debug("Creating table %s: %s.", Consts.CDefSQLiteDBTablePop, pstmt)
      c.execute(pstmt)
      self.commit()

   def resetTableIdentify(self):
      """ Delete all records on the table with the same Identify """
      c = self.getCursor()
      stmt  = "delete from %s where identify = ?" % (Consts.CDefSQLiteDBTable)
      stmt2 = "delete from %s where identify = ?" % (Consts.CDefSQLiteDBTablePop)

      logging.debug("Erasing data from the tables with the identify = %s", self.getIdentify())
      try:
         c.execute(stmt, (self.getIdentify(),))
         c.execute(stmt2, (self.getIdentify(),))
      except sqlite3.OperationalError, expt:
         if expt.message.find("no such table") >= 0:
            print "\n ## The DB Adapter can't find the tables ! Consider enable the parameter resetDB ! ##\n"

      self.commit()


   def resetStructure(self, stats):
      """ Deletes de current structure and calls createStructure

      :param stats: the statistics object

      """
      logging.debug("Reseting structure, droping table and creating new empty table.")
      c = self.getCursor()
      c.execute("drop table if exists %s" % (Consts.CDefSQLiteDBTable,))
      c.execute("drop table if exists %s" % (Consts.CDefSQLiteDBTablePop,))
      self.commit()
      self.createStructure(stats)
      
   def insert(self, stats, population, generation):
      """ Inserts the statistics data to database

      :param stats: statistics object (:class:`Statistics.Statistics`)
      :param population: population to insert stats (:class:`GPopulation.GPopulation`)
      :param generation: the generation of the insert

      """
      c = self.getCursor()
      pstmt = "insert into %s values (?, ?, " % (Consts.CDefSQLiteDBTable)
      for i in xrange(len(stats)):
         pstmt += "?, "
      pstmt = pstmt[:-2] + ")" 
      c.execute(pstmt, (self.getIdentify(), generation) + stats.asTuple())

      pstmt = "insert into %s values(?, ?, ?, ?, ?)" % (Consts.CDefSQLiteDBTablePop,)
      tups = []
      for i in xrange(len(population)):
         ind = population[i]
         tups.append((self.getIdentify(), generation, i, ind.fitness, ind.score))

      c.executemany(pstmt, tups)
      if (generation % self.commitFreq == 0):
         self.commit()

class DBXMLRPC(DBBaseAdapter):
   """ DBXMLRPC Class - Adapter to dump statistics to a XML Remote Procedure Call

   Example:
      >>> adapter = DBXMLRPC(url="http://localhost:8000/", identify="run_01",
                             frequency = 1)

      :param url: the URL of the XML RPC
      :param identify: the identify of the run
      :param frequency: the generational dump frequency


   .. note:: The XML RPC Server must implement the *insert* method, wich receives
             a python dictionary as argument.
   
   Example of an server in Python: ::

      import xmlrpclib
      from SimpleXMLRPCServer import SimpleXMLRPCServer

      def insert(l):
          print "Received statistics: %s" % l

      server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
      print "Listening on port 8000..."
      server.register_function(insert, "insert")
      server.serve_forever()

   .. versionadded:: 0.6
      The :class:`DBXMLRPC` class.

   """
   def __init__(self, url, identify=None, frequency = Consts.CDefXMLRPCStatsGenFreq):
      """ The creator of DBXMLRPC Class """

      DBBaseAdapter.__init__(self, frequency, identify)

      self.url = url
      self.proxy = None

   def __repr__(self):
      """ The string representation of adapter """
      ret = "DBXMLRPC DB Adapter [URL='%s', identify='%s']" % (self.url, self.getIdentify())
      return ret

   def open(self):
      """ Open the XML RPC Server proxy """
      logging.debug("Opening the XML RPC Server Proxy on %s", self.url)
      self.proxy = xmlrpclib.ServerProxy(self.url, allow_none=True)

   def insert(self, stats, population, generation):
      """ Calls the XML RPC procedure

      :param stats: statistics object (:class:`Statistics.Statistics`)
      :param population: population to insert stats (:class:`GPopulation.GPopulation`)
      :param generation: the generation of the insert

      """
      di = stats.internalDict.copy()
      di.update({"identify": self.getIdentify(), "generation": generation})
      self.proxy.insert(di)

