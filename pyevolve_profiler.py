# $Id: pyevolve_profiler.py 158 2009-01-20 16:22:09Z christian.perone $
import pyevolve
from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import DBAdapters
from pyevolve import Statistics

# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):
   score = 0.0

   # iterate over the chromosome
   for value in chromosome:
      if value==0:
         score += 0.5
   return score


def main_run():

   # Genome instance
   genome = G1DList.G1DList(20)
   genome.setParams(rangemin=0, rangemax=10)

   # The evaluator function (objective function)
   genome.evaluator.set(eval_func)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
#   ga.selector.set(Selectors.GRouletteWheel)
   ga.setPopulationSize(500)
   ga.nGenerations = 10

   # Create DB Adapter and set as adapter
   #sqlite_adapter = DBAdapters.DBSQLite(identify="profiler", reset=True)
   #ga.setDBAdapter(sqlite_adapter)

   # Do the evolution, with stats dump
   # frequency of 10 generations
   ga.evolve(freq_stats=1)

   # Best individual
   # print ga.bestIndividual()


import hotshot, hotshot.stats
prof = hotshot.Profile("ev.prof")
prof.runcall(main_run)
prof.close()
stats = hotshot.stats.load("ev.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

