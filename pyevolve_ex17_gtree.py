from pyevolve import GSimpleGA
from pyevolve import GTree
from pyevolve import Crossovers
from pyevolve import Mutators
import time
import random


def eval_func(chromosome):
   score = 0.0

   height = chromosome.getHeight()

   for node in chromosome:
      score += (100 - node.getData())*0.1

   if height <= chromosome.getParam("max_depth"):
      score += (score*0.8)

   return score

def main_run():

   genome = GTree.GTree()
   genome.setParams(max_depth=3, max_sister=2, method="grow")
   genome.evaluator += eval_func
   genome.crossover.set(Crossovers.GTreeCrossoverSinglePointStrict)

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setGenerations(500)
   #ga.setMutationRate(0.0)
   
   ga(freq_stats=10)
   best = ga.bestIndividual()
   print best

#import hotshot, hotshot.stats
#prof = hotshot.Profile("ev.prof")
#prof.runcall(main_run)
#prof.close()
#stats = hotshot.stats.load("ev.prof")
#stats.strip_dirs()
#stats.sort_stats('time', 'calls')
#stats.print_stats(20)

if __name__ == "__main__":
  ##import psyco
  ##psyco.full()
  t0 = time.clock()
  main_run()
  t1 = time.clock()
  print "%.3f" % (t1-t0)

