from pyevolve import GSimpleGA
from pyevolve import GTree
from pyevolve import Consts
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Util
import math
#import pydot   

rmse_accum     = Util.RMSEAccumulator()

def gp_add(a, b): return a+b
def gp_square(a): return a*a
def gp_sqrt(a):
   ret = 0   
   try:
      ret = math.sqrt(a)
   except:
      pass
   return ret
   
def eval_func(chromosome):
   global rmse_accum
   rmse_accum.reset()
   code_comp = chromosome.getCompiledCode()
   
   for a in xrange(0, 5):
      for b in xrange(0, 5):
         evaluated     = eval(code_comp)
         target        = math.sqrt((a*a)+(b*b))
         rmse_accum += (target, evaluated)

   return rmse_accum.getRMSE()

def callback_draw(ga):
   pop = ga.getPopulation()
   graph = pydot.Dot()
   gen = ga.getCurrentGeneration()

   n = 0
   for ind in pop:
      n = ind.writeDotGraph(graph, n)
   graph.write_jpeg('pop%d.tif' % gen, prog='dot')
   return False


def main_run():
   genome = GTree.GTreeGP()
   root   = GTree.GTreeNodeGP('a', Consts.nodeType["TERMINAL"])
   genome.setRoot(root)

   genome.setParams(max_depth=4, method="ramped")
   genome.evaluator += eval_func
   genome.mutator.set(Mutators.GTreeGPMutatorSubtree)

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setParams(gp_terminals       = ['a', 'b'],
                gp_function_prefix = "gp")

   ga.setMinimax(Consts.minimaxType["maximize"])
   ga.setGenerations(20)
   #ga.stepCallback.set(callback_draw)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.08)
   ga.setPopulationSize(500)
   
   ga(freq_stats=5)
   print ga.bestIndividual()

if __name__ == "__main__":
   main_run()
