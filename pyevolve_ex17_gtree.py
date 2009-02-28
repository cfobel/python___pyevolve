from pyevolve import GSimpleGA
from pyevolve import GTree
#from pyevolve import DBAdapters
import time

# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):
   score = 0.0

   for node in chromosome:
      if node.getData()==0:
         score += 0.1

   return score

def main_run():

   genome = GTree.GTree()
   genome.setParams(max_depth=3, max_sister=-2, method="full")
   genome.evaluator += eval_func

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setGenerations(100)
   
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
  #import psyco
  #psyco.full()
  t0 = time.clock()
  main_run()
  t1 = time.clock()
  print "%.3f" % (t1-t0)

