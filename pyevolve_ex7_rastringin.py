from pyevolve import G1DList, GSimpleGA
from pyevolve import Initializators, Mutators, Consts, Selectors
import math

# This is the Rastringin Function, a deception function
def rastringin(xlist):
   n = len(xlist)
   total = 0
   for i in xrange(n):
      total += xlist[i]**2 - 10*math.cos(2*math.pi*xlist[i])
   return (10*n) + total

if __name__ == "__main__":

   import psyco
   psyco.full()

   # Genome instance
   genome = G1DList.G1DList(20)
   genome.setParams(rangemin=-5.2, rangemax=5.30, bestRawScore=0.00, roundDecimal=2)
   genome.initializator.set(Initializators.G1DListInitializatorReal)
   genome.mutator.set(Mutators.G1DListMutatorRealGaussian)

   # The evaluator function (objective function)
   genome.evaluator.set(rastringin)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.setMinimax(Consts.minimaxType["minimize"])
   #ga.selector.set(Selectors.GRouletteWheel)
   ga.setGenerations(1000)
   ga.setCrossoverRate(0.8)
   ga.setPopulationSize(200)
   ga.setMutationRate(0.06)
   ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)

   # Create DB Adapter and set as adapter
   #sqlite_adapter = DBAdapters.DBSQLite(identify="rastringin")
   #ga.setDBAdapter(sqlite_adapter)

   # Do the evolution, with stats dump
   # frequency of 10 generations
   ga.evolve(freq_stats=50)

   # Best individual
   best = ga.bestIndividual()
   print "\nBest individual score: %.2f" % (best.getRawScore(),)
   #print best

