"""

:mod:`Network` -- network utility module
============================================================================

In this module you'll find all the network related implementation

.. versionadded:: 0.6
   The *Network* module.

"""
import threading
import socket
import time
import sys

def getMachineIP():
   """ Return all the IPs from current machine.

   Example:
      >>> Util.getMachineIP()
      ['200.12.124.181', '192.168.0.1']      

   :rtype: a python list with the string IPs

   .. versionadded:: 0.6
      The *getMachineIP* function.

   """
   hostname = socket.gethostname()
   addresses = socket.getaddrinfo(hostname, None)
   ips = [x[4][0] for x in addresses]
   return ips

class UDPSocketBase:
   def __init__(self, host, port, broadcast=True):
      self.recvData = None
      self.host = host
      self.port = port
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      if broadcast:
         self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
      self.sock.bind((host, port))     

   def close(self):
      self.sock.close()

   def broadcast(self, data):
      return self.sock.sendto(data, (Consts.CDefBroadcastAddress, self.port))

   def getBroadcast(self):
      self.data, self.sender = self.sock.recvfrom(1024)
      return (self.sender[0], self.data)

class UDPSocketThreadClient(UDPSocketBase, threading.Thread):
   def __init__(self, host, port, name=None):
      if name is not None:
         thread_name = "UDPSocketThreadClient-%s" % name
         threading.Thread.__init__(self, name=thread_name)
      else:
         threading.Thread.__init__(self)
      
      UDPSocketBase.__init__(self, host, port)
      self.data = None

   def setData(self, data):
      self.data = data

   def run(self):
      print "UDPSocketThreadClient: broadcasting %d bytes... " % len(self.data),
      ret = self.broadcast(self.data)
      print "%d bytes sent !" % ret
      self.close()

class UDPSocketThreadServer(UDPSocketBase, threading.Thread):
   def __init__(self, host, port):
      threading.Thread.__init__(self)
      UDPSocketBase.__init__(self, host, port)
      self.recvData = []
      self.dataLock = threading.Lock()

   def run(self):
      while True:
         data = self.getBroadcast()
         self.dataLock.acquire()
         self.recvData.append(data)
         self.dataLock.release()

   def popPool(self):
      self.dataLock.acquire()
      if len(self.recvData) >= 1:
         data = self.recvData.pop()
      else: data = None
      self.dataLock.release()
      return data

   def lenPool(self):
      self.dataLock.acquire()
      length = len(self.recvData)
      self.dataLock.release()
      return length
      

if __name__ == "__main__":
   arg = sys.argv[1]
   myself = getMachineIP()

   if arg == "server":
      s = UDPSocketThreadServer(myself[0], 666)
      s.setDaemon(True)
      s.start()
      data = s.popPool()
      while data is None:
         data = s.popPool()
         if data is not None:
            print "Recv: %s - %s" % (data[0], data[1])

   elif arg == "client":
      s = UDPSocketThreadClient(myself[0], 666)
      s.setData("sldkfslfdk")
      s.start()
      

   print "end..."


      
