import elementtree.ElementTree as ET

#import cElementTree as ET
#import lxml.etree as ET
#import xml.etree.ElementTree as ET

import random
import inspect


def getAll(tree):
   if len(tree)==0:
      return tree
   lst = []
   for it in tree:
      lst.append(getAll(it))
   return lst
   
class Tree:

   def __init__(self, func_list, terminals):
      self.func_list = func_list
      self.terminals = terminals
      self.root = ET.Element(func_list[0])
      #self.root.root = True
      self.iterRoot = self.root

   def randomSelectTerm(self):
      allNodes = getAll(self.root)
      lst = filter(lambda node: not inspect.isfunction(node.tag), allNodes)
      return random.choice(lst)

   def randomSelectNonTerm(self):
      if len(self.root)==0: return self.root

      allNodes = getAll(self.root)
      print "AllNodes: %s" % allNodes
      lst = filter(lambda node: inspect.isfunction(node.tag), allNodes)

      for node in lst:
         if len(node)==0:
            lst.remove(node)

      if len(lst) == 0: return None
      return random.choice(lst)

   def initialize(self, max_depth=10):

      if max_depth==0:
         self.iterRoot = self.randomSelectTerm()
      else:
         self.iterRoot = self.randomSelectNonTerm()

      if self.iterRoot is None: return

      if inspect.isfunction(self.iterRoot.tag):
         func_params = len(inspect.getargspec(self.iterRoot.tag)[0])
      else: func_params = 0
      
      if func_params==0: return

      for i in xrange(func_params):
         func = random.choice(self.func_list)
         term = random.choice(self.terminals)
         cho = random.choice([func, term])
         ET.SubElement(self.iterRoot, cho)
      
      self.initialize(max_depth-1)
        

def add(a, b):
   return a+b

if __name__ == "__main__":
   t = Tree([add], [2,3,4,8])
   t.initialize()
