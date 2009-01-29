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
import Util

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



class UDPThreadClient(threading.Thread):
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
      self.data = data

   def getData(self):
      return self.data

   def setTargetHost(self, host, port):
      self.target_host = host
      self.target_port = port

   def close(self):
      self.sock.close()

   def getSentBytes(self):
      sent = None
      self.sentBytesLock.acquire()
      if self.sentBytes is None:
         Util.raiseException('Bytes sent is None')
      else: sent = self.sentBytes
      self.sentBytesLock.release()
      return sent

   def send(self):
      if self.broadcast:
         return self.sock.sendto(self.data, (Consts.CDefBroadcastAddress, self.target_port))
      else:
         return self.sock.sendto(self.data, (self.target_host, self.target_port))
   
   def run(self):
      if self.data is None:
         Util.raiseException('You must set the data with setData method', ValueError)
      if self.broadcast and self.target_port is None:
         Util.raiseException('To use the broadcast, you must specify the target port', ValueError)
      if not self.broadcast and ((not self.target_host) or (not self.target_port)):
         Util.raiseException('You must specify the target host and port with setTargetHost method', ValueError)
      self.sentBytesLock.acquire()
      self.sentBytes = self.send()
      self.sentBytesLock.release()
      self.close()

class UDPThreadServer(threading.Thread):
   def __init__(self, host, port):
      threading.Thread.__init__(self)
      self.recvPool = []
      self.recvPoolLock = threading.Lock()
      self.bufferSize = 4096
      self.host = host
      self.port = port

      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.sock.bind((host, port))     

   def isReady(self):
      self.recvPoolLock.acquire()
      ret = True if len(self.recvPool) >= 1 else False
      self.recvPoolLock.release()
      return ret
    
   def poolLength(self):
      self.recvPoolLock.acquire()
      ret = len(self.recvPool)
      self.recvPoolLock.release()
      return ret

   def popPool(self):
      self.recvPoolLock.acquire()
      ret = self.recvPool.pop()
      self.recvPoolLock.release()
      return ret

   def close(self):
      self.sock.close()

   def setBufferSize(self, size):
      self.bufferSize = size

   def getBufferSize(self):
      return self.bufferSize

   def getData(self):
      try:
         data, sender = self.sock.recvfrom(self.bufferSize)
      except socket.timeout, a: return None
      return (sender[0], data)
      
   def run(self):
      while True:
         data = self.getData()
         if data == None: continue
         self.recvPoolLock.acquire()
         self.recvPool.append(data)
         self.recvPoolLock.release()
      

if __name__ == "__main__":
   arg = sys.argv[1]
   myself = getMachineIP()

   if arg == "server":
      s = UDPThreadServer('', 666)
      s.setDaemon(True)
      s.start()
      
      while True:
         print ".",
         time.sleep(10)
         if s.isReady():
            item = s.popPool()
            print item
 
   elif arg == "client":
      print "Binding on %s..." % myself[0]
      s = UDPThreadClient(myself[0], 1500, False)
      s.setData("sldkfslfdk")
      s.setTargetHost(myself[0], 666)
      s.start()
      s.join()
      print s.getSentBytes()
      

   print "end..."


      
