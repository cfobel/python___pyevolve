"""

:mod:`Util` -- utility module
============================================================================

This is the utility module, with some utility functions of general
use, like list item swap, random utilities and etc.

"""

from random import random as rand_random
from sys import platform as sys_platform
import logging
import Consts

import threading
import socket
import time
import sys

if sys_platform[:5] == "linux":
   import sys, termios
   from select import select

   fd = sys.stdin.fileno()
   new_term = termios.tcgetattr(fd)
   old_term = termios.tcgetattr(fd)
   new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)

def set_normal_term():
   """ This is a linux platform function to set the term back to normal """
   termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

def set_curses_term():
   """ This is a linux platform function to set the term to curses """
   termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

def getch():
   """ Linux platform function to get a pressed key """
   return sys.stdin.read(1)

def kbhit():
   """ The linux implementation of the kbhit() function """
   dr,dw,de = select([sys.stdin], [], [], 0)
   return dr <> []

def randomFlipCoin(p):
   """ Returns True with the *p* probability. If the *p* is 1.0,
   the function will always return True, or if is 0.0, the
   function will return always False.
   
   Example:
      >>> Util.randomFlipCoin(1.0)
      True

   :param p: probability, between 0.0 and 1.0
   :rtype: True or False

   """
   if p == 1.0: return True
   if p == 0.0: return False
   if rand_random() <= p: return True
   else: return False
   
def listSwapElement(lst, indexa, indexb):
   """ Swaps elements A and B in a list.

   Example:
      >>> l = [1, 2, 3]
      >>> Util.listSwapElement(l, 1, 2)
      >>> l
      [1, 3, 2]

   :param lst: the list
   :param indexa: the swap element A
   :param indexb: the swap element B
   :rtype: None

   """
   temp = lst[indexa]
   lst[indexa] = lst[indexb]
   lst[indexb] = temp

def list2DSwapElement(lst, indexa, indexb):
   """ Swaps elements A and B in a 2D list (matrix).

   Example:
      >>> l = [ [1,2,3], [4,5,6] ] 
      >>> Util.list2DSwapElement(l, (0,1), (1,1) )
      >>> l
      [[1, 5, 3], [4, 2, 6]]

   :param lst: the list
   :param indexa: the swap element A
   :param indexb: the swap element B
   :rtype: None

   """
   temp = lst[indexa[0]][indexa[1]]
   lst[indexa[0]][indexa[1]] = lst[indexb[0]][indexb[1]]
   lst[indexb[0]][indexb[1]] = temp

def raiseException(message, expt=None):
   """ Raise an exception and logs the message.

   Example:
      >>> Util.raiseException('The value is not an integer', ValueError)

   :param message: the message of exception
   :param expt: the exception class
   :rtype: None

   """
   logging.critical(message)
   if expt is None:
      raise Exception(message)
   else:
      raise expt, message


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
      self.sock.sendto(data, (Consts.CDefBroadcastAddress, self.port))

   def getBroadcast(self):
      self.data, self.sender = self.sock.recvfrom(1024)
      return (self.sender[0], self.data)

class UDPSocketThreadClient(UDPSocketBase, threading.Thread):
   def __init__(self, host, port):
      threading.Thread.__init__(self)
      UDPSocketBase.__init__(self, host, port)
      self.data = None

   def setData(self, data):
      self.data = data

   def run(self):
      self.broadcast(self.data)
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

if __name__ == "__main__":
   arg = sys.argv[1]

   if arg == "server":
      s = UDPSocketThreadServer(getMachineIP()[0], 666)
      s.setDaemon(True)
      s.start()
      data = s.popPool()
      while data is None:
         data = s.popPool()
         if data is not None:
            print "Recv: %s - %s" % (data[0], data[1])

   elif arg == "client":
      s = UDPSocketThreadClient(getMachineIP()[0], 666)
      s.setData("sldkfslfdk")
      s.start()
      

   print "end..."


      



