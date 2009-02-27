from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import DBAdapters
from pyevolve import Util

# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):
   score = 0.0
   all_nodes = chromosome.getAllNodes()

   for n in all_nodes:
      if n.getData()==0:
         score += 1

   score += (6-chromosome.getHeight())*0.1

   return score

if __name__ == "__main__":

   genome = GTree.GTree()
   genome.setParams(max_depth=6, max_sister=2, method="grow")
   genome.evaluator += eval_func

   ga = GSimpleGA.GSimpleGA(genome)

   #ga.selector.set(Selectors.GRouletteWheel)
   ga.setGenerations(30)
   
   #sqlite_adapter = DBAdapters.DBSQLite(identify="ex1")
   #ga.setDBAdapter(sqlite_adapter)

   # Do the evolution, with stats dump
   # frequency of 20 generations

   ga(freq_stats=10)
   best = ga.bestIndividual()
   print best
