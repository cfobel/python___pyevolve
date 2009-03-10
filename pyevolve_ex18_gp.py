from pyevolve import GSimpleGA
from pyevolve import GTree
from time import clock
from random import randint

def gp_random(a,b):
   return randint(a,b)

def gp_sub(a,b):
   return a-b

def gp_add(a,b):
   return a+b

def eval_func(chromosome):
   xpr   = chromosome.getPreOrderExpression()
   score = 0.0

   ret    = eval(xpr)
   score += abs(ret)

   return score

def main_run():
   import psyco
   psyco.full()

   genome = GTree.GTreeGP()
   genome.setParams(max_depth=3, method="full")
   genome.evaluator += eval_func

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setParams(gp_terminals  = ['1.', '2.', '3.', '4.'],
                gp_func_prefix= "gp")

   ga.setGenerations(100)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.1)
   
   ga(freq_stats=10)
   best = ga.bestIndividual()
   print best


if __name__ == "__main__":
  t0 = clock()
  main_run()
  t1 = clock()
  print "%.3f" % (t1-t0)

