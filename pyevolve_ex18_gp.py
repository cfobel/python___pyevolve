from pyevolve import GSimpleGA
from pyevolve import GTree
from pyevolve import Consts
from pyevolve import Selectors
from math import sqrt

def gp_add(a, b): return a+b
def gp_sqrt(a):   return sqrt(a)
def gp_square(a): return a*a
   
def eval_func(chromosome):
   score  = 0.0
   expr    = chromosome.getPreOrderExpression()
   for a in xrange(1,8):
      for b in xrange(1,8):
         target = sqrt((a*a)+(b*b))
         ret    = eval(expr)
         score += (target - ret)**2
   return score

def main_run():
   genome = GTree.GTreeGP()
   genome.setParams(max_depth=6, method="grow")
   genome.evaluator += eval_func

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setParams(gp_terminals  = ['a', 'b'],
                gp_func_prefix= "gp")

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.selector.set(Selectors.GRouletteWheel)
   ga.setGenerations(5000)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.6)
   ga.setPopulationSize(200)
   
   ga(freq_stats=5)
   best = ga.bestIndividual()
   print best

if __name__ == "__main__":
   main_run()
