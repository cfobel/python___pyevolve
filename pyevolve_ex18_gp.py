from pyevolve import GSimpleGA
from pyevolve import GTree
from pyevolve import Consts
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Util
import math
import random

rmse_accum = Util.RMSEAccumulator()

@GTree.gpdec(representation="+", color="red")
def gp_add(a, b): return a+b

@GTree.gpdec(representation="-")
def gp_sub(a, b): return a-b

@GTree.gpdec(representation="*")
def gp_mul(a, b): return a*b

@GTree.gpdec(representation="sqrt")
def gp_sqrt(a):   return math.sqrt(abs(a))
   
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

def callback_draw(ga_engine):
   GTree.writeGTreeGPPopulation(ga_engine, "full.jpg")
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
   ga.selector.set(Selectors.GRouletteWheel)

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(1)
   ga.stepCallback.set(callback_draw)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.08)
   ga.setPopulationSize(10)
   
   ga(freq_stats=10)
   #print ga.bestIndividual()

if __name__ == "__main__":
   main_run()
