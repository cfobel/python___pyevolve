from pyevolve import GSimpleGA
from pyevolve import GTree
from pyevolve import Consts
from pyevolve import Selectors
from pyevolve import Mutators
from math import sqrt
import pydot   

def gp_add(a, b): return a+b
def gp_square(a): return a*a
def gp_sqrt(a):
   ret = 0   
   try:
      ret = sqrt(a)
   except:
      pass
   return ret
   
def eval_func(chromosome):
   square_accum  = 0.0
   code_comp     = chromosome.getCompiledCode()
   
   for a in xrange(-5, 5):
      for b in xrange(-5, 5):
         target        = sqrt((a*a)+(b*b))
         ret           = eval(code_comp)
         square_accum += (target - ret)**2

   RMSE = sqrt(square_accum / 100.0)
   score = (1.0 / (RMSE+1.0))
   return score

def main_run():
   genome = GTree.GTreeGP()
   root   = GTree.GTreeNodeGP('a', Consts.nodeType["TERMINAL"])
   genome.setRoot(root)

   genome.setParams(max_depth=4, method="ramped")
   genome.evaluator += eval_func
   genome.mutator.set(Mutators.GTreeGPMutatorSubtree)
   #genome.mutator.add(Mutators.GTreeGPMutatorOperation)

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setParams(gp_terminals  = ['a', 'b'],
                gp_func_prefix= "gp")

   ga.setMinimax(Consts.minimaxType["maximize"])
   ga.setGenerations(1000)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.08)
   ga.setPopulationSize(200)
   
   ga(freq_stats=10)
   #print ga.bestIndividual()

   graph = pydot.Dot()
   ga.bestIndividual().writeDotGraph(graph)
   graph.write_jpeg('tree.png', prog='dot')

if __name__ == "__main__":
   main_run()
