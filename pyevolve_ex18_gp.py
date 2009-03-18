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
   score    = 0.0
   code_comp = chromosome.getCompiledCode()
   
   for a in xrange(1, 8):
      for b in xrange(1, 8):
         target = sqrt((a*a)+(b*b))+a+b
         ret    = eval(code_comp)
         score += (target - ret)**2

   return score

def main_run():
   genome = GTree.GTreeGP()
   root   = GTree.GTreeNodeGP('a', Consts.nodeType["TERMINAL"])
   genome.setRoot(root)

   genome.setParams(max_depth=8, method="grow")
   genome.evaluator += eval_func
   genome.mutator.set(Mutators.GTreeGPMutatorSubtree)

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setParams(gp_terminals  = ['a', 'b'],
                gp_func_prefix= "gp")

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.selector.set(Selectors.GRouletteWheel)
   ga.setGenerations(1000)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.2)
   ga.setPopulationSize(200)
   
   ga(freq_stats=20)

   graph = pydot.Dot()
   ga.bestIndividual().writeDotGraph(graph)
   graph.write_jpeg('tree.png', prog='dot')

if __name__ == "__main__":
   main_run()
#   import hotshot, hotshot.stats
#   prof = hotshot.Profile("ev.prof")
#   prof.runcall(main_run)
#   prof.close()
#   stats = hotshot.stats.load("ev.prof")
#   stats.strip_dirs()
#   stats.sort_stats('time', 'calls')
#   stats.print_stats(20)

