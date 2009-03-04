from pyevolve import G1DList, GSimpleGA, Selectors, Statistics
from pyevolve import Initializators, Mutators, Consts, DBAdapters

# This is the Rosenbrock Function, a deception function
def rosenbrock(xlist):
   sum_var = 0
   for x in xrange(1, len(xlist)):
      sum_var += 100.0 * (xlist[x] - xlist[x-1]**2)**2 + (1 - xlist[x-1])**2
   return sum_var

if __name__ == "__main__":

   # Genome instance
   genome = G1DList.G1DList(10)
   genome.setParams(rangemin=-5, rangemax=10, bestRawScore=0.0)
   genome.mutator.set(Mutators.G1DListMutatorIntegerRange)

   # The evaluator function (objective function)
   genome.evaluator.set(rosenbrock)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.setMinimax(Consts.minimaxType["minimize"])
   #ga.selector.set(Selectors.GRouletteWheel)
   ga.setGenerations(5000)
   ga.setCrossoverRate(0.6)
   ga.setPopulationSize(400)
   ga.setMutationRate(0.08)
   ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)

   # Create DB Adapter and set as adapter
   #sqlite_adapter = DBAdapters.DBSQLite(identify="rosenbrock")
   #ga.setDBAdapter(sqlite_adapter)

   # Do the evolution, with stats dump
   # frequency of 10 generations
   ga.evolve(freq_stats=50)

   # Best individual
   best = ga.bestIndividual()
   print "\nBest individual score: %.2f" % (best.score,)
   print best















