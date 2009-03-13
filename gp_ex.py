from pyevolve import GSimpleGA
from pyevolve import GTree
from pyevolve import Consts
from pyevolve import Selectors
from math import sqrt, pow, exp

def gp_add(a, b): return a+b
def gp_sub(a, b): return a-b

def gp_sqrt(a):
   """ Protected square root """
   try:
      ret = sqrt(a)
   except:
      ret = 0
   return ret


def gp_exp(a):
   """ Protected exp, e^a """
   try:
      ret = exp(a)
   except:
      ret = 0
   return ret

def gp_pow(a,b):
   """ Protected power, a^b """
   try:
      ret = pow(a, b)
   except:
      ret = 0
   return ret
   
def eval_func(chromosome):
   """ Our evaluation function """
   score  = 0.0
   expr   = chromosome.getPreOrderExpression()
   for a in xrange(1,5):
      for b in xrange(1,5):

         target = pow(a,b)+2
         ret    = eval(expr)
         try:
            score += (target - ret)**2
         except:
            score += 5000
   return score

def main_run():
   genome = GTree.GTreeGP()
   genome.setParams(max_depth=3, method="grow")
   genome.evaluator += eval_func

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setParams(gp_terminals  = ['a', 'b', '2', '3', '4'],
                gp_func_prefix= "gp")

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(500)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.09)
   
   ga(freq_stats=10)
   best = ga.bestIndividual()
   print best

if __name__ == "__main__":
   main_run()
