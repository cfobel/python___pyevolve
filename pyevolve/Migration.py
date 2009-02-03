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

class MigrationScheme:
   """ This is the base class for all migration schemes
   
   :param host: the source hostname
   :param port: the source host port
   """

   def __init__(self, host, port):
      self.myself = None
      self.groupName = None
      self.setMyself(host, port)

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
   
   def exchange(self, ga_engine):
      """ Exchange individuals
      
      :param ga_engine: the GA Engine
      """
      pass


class WANMigration(MigrationScheme):
   """ This is the Simple Migration class for distributed GA

   Example:
      >>> mig = WANMigration("192.168.0.1", "10000")
   
   :param host: the source hostname
   :param port: the source port number
   """

   def __init__(self, host, port):
      MigrationSchemeBase.__init__(self, host, port)
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
      for thr in self.clientThreads:
         thr.join(5)
         if thr.isAlive(): print "warning: some threads have not joined !"

   def exchange(self, ga_engine):
      """ This is the main method, is where the individuals
      are exchanged
      
      :param ga_engine: the GA Engine
      """
      clientThread = Network.UDPThreadUnicastClient(self.myself[0], rand_randint(30000, 65534))
      self.clientThreads.append(clientThread)

      # TODO
      # Who will migrate ? Selection stage..
      # Set the targets based on topology, etc...
      # Send individuals..
      # Check if there is individuals on the server pool
      # Who will migrate to local population ? Who will be replaced ?
