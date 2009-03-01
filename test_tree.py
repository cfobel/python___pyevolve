#from pyevolve import *
from pyevolve import Util, GTree, Crossovers
from timeit import Timer

def test_run():
   a = GTree.GTree()
   a.setParams(max_depth=5, max_sister=2, method="grow")
   #a.initializator.set(Initializators.GTreeInitInteger)
   #a.mutator.set(Mutators.GTreeMutatorIntegerRange)

   for i in xrange(100):
      a.initialize()
      print a.getHeight()
      if a.getHeight()==0:
         print a
         

if __name__ == "__main__":
   #t = Timer("test_run()", "from __main__ import test_run")
   #print t.timeit(100)
   test_run()




