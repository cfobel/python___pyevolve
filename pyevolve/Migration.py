"""
:mod:`Migration` -- the migration schemes, distributed GA
=====================================================================

This module contains all the migration schemes and the distributed
GA related functions.

.. versionadded:: 0.6
   The :mod:`Migration` module.

"""

from Util import Graph
from random import randint as rand_randint
import Network
import Consts
from FunctionSlot import FunctionSlot

class MigrationScheme:
   """ This is the base class for all migration schemes
   
   :param host: the source hostname
   :param port: the source host port
   """

   selector = None
   """ This is the function slot for the selection method
   if you want to change the default selector, you must do this: ::

      migration_scheme.selector.set(Selectors.GRouletteWheel) """

   def __init__(self, host, port):
      self.myself = None
      self.groupName = None
      self.selector = FunctionSlot("Selector")
      self.setMyself(host, port)
      self.GAEngine = None
      self.nMigrationRate = Consts.CDefGenMigrationRate

   def setMigrationRate(self, generations):
      """ Sets the generation frequency supposed to migrate
      and receive individuals.

      :param generations: the number of generations      
      """
      self.nMigrationRate = generations

   def getMigrationRate(self):
      """ Return the the generation frequency supposed to migrate
      and receive individuals
      
      :rtype: the number of generations
      """
      return self.nMigrationRate

   def setGAEngine(self, ga_engine):
      """ Sets the GA Engine handler """
      self.GAEngine = ga_engine

   def start(self):
      """ Initializes the migration scheme """
      pass

   def stop(self):
      """ Stops the migration engine """
      pass

   def setGroup(self, name):
      """ Sets the group name
      
      :param name: the group name

      .. note:: all islands of evolution which are supposed to exchange
                individuals, must have the same group name.
      """
      self.groupName = name

   def setMyself(self, host, port):
      """ Which interface you will use to send/receive data
      
      :param host: your hostname
      :param port: your port
      """
      self.myself = (host, port)

   def select(self):
      """ Pickes an individual from population using specific selection method
      
      :rtype: an individual object
      """
      if self.selector.isEmpty():
         return self.GAEngine.select(popID=self.GAEngine.currentGeneration)
      else:
         for it in self.selector.applyFunctions(self.GAEngine.internalPop, popID=self.GAEngine.currentGeneration):
            return it

   def exchange(self):
      """ Exchange individuals """
      pass

class WANMigration(MigrationScheme):
   """ This is the Simple Migration class for distributed GA

   Example:
      >>> mig = WANMigration("192.168.0.1", "10000")
   
   :param host: the source hostname
   :param port: the source port number
   """

   selector = None
   """ This is the function slot for the selection method
   if you want to change the default selector, you must do this: ::

      migration_scheme.selector.set(Selectors.GRouletteWheel) """

   def __init__(self, host, port):
      MigrationScheme.__init__(self, host, port)
      self.topologyGraph = None
      self.serverThread = Network.UDPThreadServer(host, port)
      self.clientThreads = []

   def setTopology(self, graph):
      """ Sets the topology of the migrations
      
      :param graph: the :class:`Util.Graph` instance
      """
      self.topologyGraph = graph

   def start(self):
      """ Start capture of packets and initialize the migration scheme """
      self.serverThread.start()

   def stop(self):
      """ Stops the migration engine """
      self.serverThread.shutdown()
      timeout = self.serverThread.timeout
      self.serverThread.join(timeout+3)
      if self.serverThread.isAlive():
         print "warning: server thread not joined !"
      for thr in self.clientThreads:
         try:
            thr.join(5)
         except RuntimeError:
            pass
         if thr.isAlive(): print "warning: client thread not joined !"

   def exchange(self):
      """ This is the main method, is where the individuals
      are exchanged """
      #clientThread = Network.UDPThreadUnicastClient(self.myself[0], rand_randint(30000, 65534))
      #self.clientThreads.append(clientThread)

      # print self.select()

      # TODO
      # Who will migrate ? Selection stage..
      # Set the targets based on topology, etc...
      # Send individuals..
      # Check if there is individuals on the server pool
      # Who will migrate to local population ? Who will be replaced ?
