from pyevolve import GSimpleGA
from pyevolve import GTree
from pyevolve import Crossovers
from pyevolve import Mutators
from pyevolve import Initializators
import time
import random


def eval_func(chromosome):
   score = 0.0
   xpr = chromosome.getNExpression()
   y = 0.5

   try:
      ret = eval(xpr)
   except:
      ret = 0.0

   score += abs(ret)

   return score

def main_run():

   genome = GTree.GTreeGP()
   genome.setParams(max_depth=5, method="grow")
   genome.evaluator += eval_func

   ga = GSimpleGA.GSimpleGA(genome)
   #ga.setGenerations(100)
   #ga.setMutationRate(0.05)
   
   ga(freq_stats=10)
   best = ga.bestIndividual()
   print best
   print best.getNExpression()


if __name__ == "__main__":
  t0 = time.clock()
  main_run()
  t1 = time.clock()
  print "%.3f" % (t1-t0)

