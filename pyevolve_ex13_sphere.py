from pyevolve import *
import math

# This is the Sphere Function
def sphere(xlist):
   #n = len(xlist)
   #total = 0
   #for i in xrange(n):
   #   total += (xlist[i]**2)
   total = 0
   for i in xlist:
      total += i**2

   return total


def run_main():
   # Genome instance
   genome = G1DList.G1DList(140)
   genome.setParams(rangemin=-5.12, rangemax=5.13)
   genome.initializator.set(Initializators.G1DListInitializatorReal)
   genome.mutator.set(Mutators.G1DListMutatorRealGaussian)

   # The evaluator function (objective function)
   genome.evaluator.set(sphere)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome, seed=666)
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(1500)
   ga.setMutationRate(0.01)

   # Do the evolution, with stats dump
   # frequency of 10 generations
   ga.evolve(freq_stats=500)

   # Best individual
   best = ga.bestIndividual()

if __name__ == "__main__":
   run_main()
   

