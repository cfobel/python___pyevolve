from pyevolve import GSimpleGA
from pyevolve import GTree
from pyevolve import Consts
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Util
from math import sqrt

rmse_accum     = Util.RMSEAccumulator()

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
PRIMES_LEN = len(PRIMES)

def prot_sqrt(v):
   ret = 0   
   try:
      ret = sqrt(v)
   except:
      pass
   return ret

def gp_add(a, b): return a+b
def gp_sub(a, b): return a-b
def gp_square(a): return a*a
def gp_div(a, b): return 0 if b==0 else a/b
def gp_mul(a, b): return a*b
def gp_sqrt(a):   return prot_sqrt(a)
def gp_max(a,b): return a if a>b else b
   
def eval_func(chromosome):
   global rmse_accum
   rmse_accum.reset()

   code_comp     = chromosome.getCompiledCode()

   for x in xrange(PRIMES_LEN):
      a = x+1
      ret = int(round(eval(code_comp)))
      rmse_accum += (PRIMES[x], ret)

   return rmse_accum.getRMSE()

def main_run():
   genome = GTree.GTreeGP()
   root   = GTree.GTreeNodeGP('a', Consts.nodeType["TERMINAL"])
   genome.setRoot(root)

   genome.setParams(max_depth=8, method="ramped")
   genome.evaluator += eval_func
   genome.mutator.set(Mutators.GTreeGPMutatorSubtree)

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setParams(gp_terminals       = ['a'],
                gp_function_prefix = "gp")

   ga.setMinimax(Consts.minimaxType["maximize"])
   ga.setGenerations(5000)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.08)
   ga.setPopulationSize(4000)
   
   ga(freq_stats=2)
   print ga.bestIndividual()

def funx(a):
   return gp_sqrt(gp_add(gp_div(gp_add(gp_add(gp_div(gp_add(a, gp_mul(a, a)), gp_sqrt(a)), gp_div(gp_square(gp_mul(a, a)), gp_square(a))), gp_div(gp_square(gp_mul(gp_sqrt(a), gp_square(a))), gp_add(gp_mul(a, a), gp_div(gp_square(a), gp_square(a))))), gp_sqrt(gp_sqrt(a))), gp_square(gp_sqrt(gp_mul(gp_div(gp_mul(gp_div(a, a), gp_div(a, a)), gp_add(gp_mul(a, a), gp_sqrt(a))), gp_mul(gp_mul(gp_mul(a, a), gp_div(a, a)), gp_square(gp_add(a, a))))))))

def main_test():
   ret = funx(1098)
   print int(round(ret))
   ret = funx(1099)
   print int(round(ret))
   ret = funx(1100)
   print int(round(ret))

if __name__ == "__main__":
   main_run()
   #main_test()
