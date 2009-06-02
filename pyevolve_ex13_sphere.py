from pyevolve import *
import math

# This is the Sphere Function
def sphere(xlist):
   n = len(xlist)
   total = 0
   for i in range(n):
      total += (xlist[i]**2)
   return total


if __name__ == "__main__":
   
   #import psyco
   #psyco.full()

   # Genome instance
   genome = G1DList.G1DList(50)
   genome.setParams(rangemin=-5.12, rangemax=5.13, bestrawscore=0.00, rounddecimal=2)
   genome.initializator.set(Initializators.G1DListInitializatorReal)
   genome.mutator.set(Mutators.G1DListMutatorRealGaussian)

   # The evaluator function (objective function)
   genome.evaluator.set(sphere)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(1500)
   ga.setMutationRate(0.02)
   ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)

   # Create DB Adapter and set as adapter
   # sqlite_adapter = DBAdapters.DBSQLite(identify="sphere")
   # ga.setDBAdapter(sqlite_adapter)

   # Do the evolution, with stats dump
   # frequency of 10 generations
   ga.evolve(freq_stats=40)

   # Best individual
   best = ga.bestIndividual()
   print "\nBest individual score: %.2f" % (best.score,)
   print best

