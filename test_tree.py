#from pyevolve import *
from pyevolve import Util, GTree, Crossovers

#from timeit import Timer

def test_run():
   a = GTree.GTree()
   a.setParams(max_depth=2, max_sister=-2, method="full")
   #a.initializator.set(Initializators.GTreeInitInteger)
   #a.mutator.set(Mutators.GTreeMutatorIntegerRange)
   a.initialize()
   b = a.clone()
   b.initialize()
   
   
   sister, brother = Crossovers.GTreeCrossoverSinglePoint(None, mom=a, dad=b, count=2)



#   print tlist

if __name__ == "__main__":
   #t = Timer("test_run()", "from __main__ import test_run")
   #print t.timeit(1)
   test_run()




