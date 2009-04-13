from pyevolve import GSimpleGA
from pyevolve import GTree
from pyevolve import Consts
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Util
import math
#import pydot

rmse_accum     = Util.RMSEAccumulator()

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
PRIMES_LEN = len(PRIMES)

def gp_sum(a):    return a*(a+1)/2
def gp_add(a, b): return a+b
def gp_sub(a, b): return a-b
def gp_square(a): return a*a
def gp_div(a, b): return 1 if b==0 else a/b
def gp_mul(a, b): return a*b
def gp_sqrt(a):   return math.sqrt(abs(a))
def gp_mod(a,b):  return 1 if b==0 else a%b
def gp_cos(a):    return math.cos(a)
def gp_sin(a):    return math.sin(a)
def gp_ifltz(a, b, c): return b if a < 0 else c

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
   print "Starting for %d primes !" % PRIMES_LEN
   genome = GTree.GTreeGP()
   root   = GTree.GTreeNodeGP('a', Consts.nodeType["TERMINAL"])
   genome.setRoot(root)

   genome.setParams(max_depth=10, method="ramped")
   genome.evaluator += eval_func
   genome.mutator.set(Mutators.GTreeGPMutatorSubtree)

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setParams(gp_terminals       = ['a', 'ephemeral:random.random()', 'math.pi', 'math.e'],
                gp_function_prefix = "gp")

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(5000)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.08)
   ga.setPopulationSize(2000)
   
   ga(freq_stats=5)
   best = ga.bestIndividual()
   print best

   #graph = pydot.Dot()
   #best.writeDotGraph(graph)
   #graph.write_jpeg('best.jpg', prog='dot')
  

def funx(a):
   return gp_add(gp_div(gp_sum(a), gp_sqrt(a)), gp_sqrt(gp_square(a)))

def main_test():
   for i in xrange(PRIMES_LEN):
      ret = int(round(funx(i+1)))
      print "[%03d] [%03d] / Error = %d" % (PRIMES[i], ret, PRIMES[i]-ret)

if __name__ == "__main__":
   main_run()
   #main_test()
