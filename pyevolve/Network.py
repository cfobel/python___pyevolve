"""

:mod:`Network` -- network utility module
============================================================================

In this module you'll find all the network related implementation

.. versionadded:: 0.6
   The *Network* module.

"""
from __future__ import with_statement
import threading
import socket
import time
import sys
import Util
import cPickle, zlib
import Consts

def getMachineIP():
   """ Return all the IPs from current machine.

   Example:
      >>> Util.getMachineIP()
      ['200.12.124.181', '192.168.0.1']      

   :rtype: a python list with the string IPs

   """
   hostname = socket.gethostname()
   addresses = socket.getaddrinfo(hostname, None)
   ips = [x[4][0] for x in addresses]
   return ips



class UDPThreadClient(threading.Thread):
   """ The UDP client thread class.

   This class is a thread to serve as Pyevolve client on the UDP
   datagrams, it is used to send data over network lan/wan.

   Example:
      >>> s = Network.UDPThreadClient('192.168.0.2', 1500, False)
      >>> s.setData("Test data")
      >>> s.setTargetHost('192.168.0.50', 666)
      >>> s.start()
      >>> s.join()

   :param host: the hostname to bind the socket on sender (this is not the target host)
   :param port: the sender port (this is not the target port)
   :param broadcast: True or False

   """
   def __init__(self, host, port, broadcast):
      threading.Thread.__init__(self)
      self.host = host
      self.port = port
      self.target_host = None
      self.target_port = None
      self.broadcast = broadcast
      self.data = None
      self.sentBytes = None
      self.sentBytesLock = threading.Lock()

      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      if broadcast:
         self.target_host = Consts.CDefBroadcastAddress
         self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
      self.sock.bind((host, port))     

   def setData(self, data):
      """ Set the data to send

      :param data: the data to send

      """
      self.data = data

   def getData(self):
      """ Get the data to send

      :rtype: data to send

      """
      return self.data

   def setTargetHost(self, host, port):
      """ Set the host/port of the target, the destination

      :param host: the target host
      :param port: the target port

      .. note:: the host will be ignored when using broadcast mode
      
      """
      self.target_host = host
      self.target_port = port

   def close(self):
      """ Close the internal socket """
      self.sock.close()

   def getSentBytes(self):
      """ Returns the number of sent bytes. The use of this method makes sense 
      when you already have sent the data
         
      :rtype: sent bytes

      """
      sent = None
      with self.sentBytesLock:
         if self.sentBytes is None:
            Util.raiseException('Bytes sent is None')
         else: sent = self.sentBytes
      return sent

   def send(self):
      """ Send the data; this method will detect if is a broadcast or unicast. """
      if self.broadcast:
         return self.sock.sendto(self.data, (Consts.CDefBroadcastAddress, self.target_port))
      else:
         return self.sock.sendto(self.data, (self.target_host, self.target_port))
   
   def run(self):
      """ Method called when you call *.start()* of the thread """
      if self.data is None:
         Util.raiseException('You must set the data with setData method', ValueError)
      if self.broadcast and self.target_port is None:
         Util.raiseException('To use the broadcast, you must specify the target port', ValueError)
      if not self.broadcast and ((not self.target_host) or (not self.target_port)):
         Util.raiseException('You must specify the target host and port with setTargetHost method', ValueError)

      with self.sentBytesLock:
         self.sentBytes = self.send()
      self.close()

class UDPThreadServer(threading.Thread):
   """ The UDP server thread class.

   This class is a thread to serve as Pyevolve server on the UDP
   datagrams, it is used to receive data from network lan/wan.

   Example:
      >>> s = UDPThreadServer("192.168.0.2", 666, 10)
      >>> s.start()
      >>> s.shutdown()

   :param host: the host to bind the server
   :param port: the server port to bind
   :param poolSize: the size of the server pool
   :param timeout: the socket timeout

   .. note:: this thread implements a pool to keep the received data,
             the *poolSize* parameter specifies how much individuals
             we must keep on the pool until the *popPool* method 
             is called; when the pool is full, the sever will
             discard the received individuals.

   """
   def __init__(self, host, port, poolSize, timeout=5):
      threading.Thread.__init__(self)
      self.recvPool = []
      self.recvPoolLock = threading.Lock()
      self.bufferSize = 4096
      self.host = host
      self.port = port
      self.timeout = timeout
      self.doshutdown = False
      self.poolSize = 10

      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.sock.bind((host, port))     
      self.sock.settimeout(self.timeout)

   def shutdown(self):
      """  Shutdown the server thread, when called, this method will stop
      the thread on the next socket timeout """
      self.doshutdown = True

   def isReady(self):
      """ Returns True when there is data on the pool or False when not
         
      :rtype: boolean
      
      """
      with self.recvPoolLock:
         ret = True if len(self.recvPool) >= 1 else False
      return ret
    
   def poolLength(self):
      """ Returns the size of the pool
      
      :rtype: integer

      """
      with self.recvPoolLock:
         ret = len(self.recvPool)
      return ret

   def popPool(self):
      """ Return the last data received on the pool

      :rtype: object

      """
      with self.recvPoolLock:
         ret = self.recvPool.pop()
      return ret

   def close(self):
      """ Closes the internal socket """
      self.sock.close()

   def setBufferSize(self, size):
      """ Sets the receive buffer size
      
      :param size: integer

      """
      self.bufferSize = size

   def getBufferSize(self):
      """ Gets the current receive buffer size

      :rtype: integer

      """
      return self.bufferSize

   def getData(self):
      """ Calls the socket *recvfrom* method and waits for the data,
      when the data is received, the method will return a tuple
      with the IP of the sender and the data received. When a timeout
      exception occurs, the method return None.
      
      :rtype: tuple (sender ip, data) or None when timeout exception

      """
      try:
         data, sender = self.sock.recvfrom(self.bufferSize)
      except socket.timeout, a: return None
      return (sender[0], data)
      
   def run(self):
      """ Called when the thread is started by the user. This method
      is the main of the thread, when called, it will enter in loop
      to wait data or shutdown when needed.
      """
      while True:
         # Get the data
         data = self.getData()
         # Shutdown called
         if self.doshutdown: break
         # The pool is full
         if self.poolLength() >= self.poolSize:
            continue
         # There is no data received
         if data == None: continue
         # It's a packet from myself
         if data[0] == self.host:
            continue
         with self.recvPoolLock:
            self.recvPool.append(data)


def pickleAndCompress(obj, level=9):
   """ Pickles the object and compress the dumped string with zlib
   
      :param obj: the object to be pickled
      :param level: the compression level, 9 is the best.

   .. versionadded:: 0.6
      The *pickleAndCompress* function

   """
   pickled = cPickle.dumps(obj)
   pickled_zlib = zlib.compress(pickled, level)
   return pickled_zlib

if __name__ == "__main__":
   arg = sys.argv[1]
   myself = getMachineIP()

   if arg == "server":
      s = UDPThreadServer(myself[0], 666)
      s.start()
      
      while True:
         print ".",
         time.sleep(10)
         if s.isReady():
            item = s.popPool()
            print item
         time.sleep(4)
         s.shutdown()
         break


   elif arg == "client":
      print "Binding on %s..." % myself[0]
      s = UDPThreadClient(myself[0], 1500, False)
      s.setData("dsfssdfsfddf")
      s.setTargetHost(myself[0], 666)
      s.start()
      s.join()
      print s.getSentBytes()
      

   print "end..."


      
