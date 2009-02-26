from pyevolve import *


def test_run():
   a = GTree.GTree()
   a.setParams(max_depth=2, max_sister=-2, method="full")
   #a.initializator.set(Initializators.GTreeInitInteger)
   #a.mutator.set(Mutators.GTreeMutatorIntegerRange)
   a.initialize()
   print a
   
   for i in xrange(20000): 
      for i in xrange(len(a)):
         x = a[i]






if __name__ == "__main__":
   from timeit import Timer
   t = Timer("test_run()", "from __main__ import test_run")
   print t.timeit(1)




