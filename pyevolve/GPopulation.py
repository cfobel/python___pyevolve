"""
:mod:`GPopulation` -- the population module
================================================================

This module contains the :class:`GPopulation.GPopulation` class, which is reponsible
to keep the population and the statistics.

Default Parameters
-------------------------------------------------------------

*Sort Type*
   
   >>> Consts.sortType["scaled"]

   The scaled sort type

*Minimax*

   >>> Consts.minimaxType["maximize"]

   Maximize the evaluation function

*Scale Method*

   :func:`Scaling.LinearScaling`

   The Linear Scaling scheme

Class
-------------------------------------------------------------


"""

import Consts, Util
from FunctionSlot import FunctionSlot
from Statistics import Statistics
from math import sqrt as math_sqrt
import logging

try:
   from multiprocessing import cpu_count, Queue, Process
   CPU_COUNT = cpu_count()
   MULTI_PROCESSING = True if CPU_COUNT > 1 else False
except:
   MULTI_PROCESSING = False

def async_eval(population, q):
   """ Internal used by the multiprocessing """
   for ind in population:
      ind.evaluate()
   q.put(population)

class GPopulation:
   """ GPopulation Class - The container for the population

   **Examples**
      Get the population from the :class:`GSimpleGA.GSimpleGA` (GA Engine) instance
         >>> pop = ga_engine.getPopulation()

      Get the best fitness individual
         >>> bestIndividual = pop.bestFitness()

      Get the best raw individual
         >>> bestIndividual = pop.bestRaw()

      Get the statistics from the :class:`Statistics.Statistics` instance
         >>> stats = pop.getStatistics()
         >>> print stats["rawMax"]
         10.4

      Iterate, get/set individuals
         >>> for ind in pop:
         >>>   print ind
         (...)
         
         >>> for i in xrange(len(pop)):
         >>>    print pop[i]
         (...)

         >>> pop[10] = newGenome
         >>> pop[10].fitness
         12.5

   :param genome: the :term:`Sample genome`

   """

   def __init__(self, genome):
      """ The GPopulation Class creator """

      logging.debug("New population instance, %s class genomes.", genome.__class__.__name__)
      self.oneSelfGenome = genome
      self.internalPop   = []
      self.internalPopRaw = []
      self.popSize       = 0
      self.sortType      = Consts.CDefPopSortType
      self.sorted        = False
      self.minimax       = Consts.CDefPopMinimax
      self.scaleMethod   = FunctionSlot("Scale Method")
      self.scaleMethod.set(Consts.CDefPopScale)
      self.allSlots      = [self.scaleMethod]

      self.internalParams = {}
      self.multiProcessing = False

      # Statistics
      self.statted = False
      self.stats   = Statistics()

   def setParams(self, **args):
      """ Set the internal params

      Example:
         >>> population.setParams(parameter="value")

      :param args: this params will saved in every chromosome for genetic op. use

      .. versionadded: 0.6
         The method `setParams'

      """
      self.internalParams.update(args)

   def getParam(self, key, nvl=None):
      """ Gets an internal parameter

      Example:
         >>> population.getParam("parameter")
         "value"

      :param key: the key of param
      :param nvl: if the key doesn't exist, the nvl will be returned

      .. versionadded: 0.6
         The method `getParam'

      """
      return self.internalParams.get(key, nvl)
      

   def setMultiProcessing(self, flag=True):
      """ Sets the flag to enable/disable the use of python multiprocessing module.
      Use this option when you have more than one core on your CPU and when your
      evaluation function is very slow.

      :param flag: True (default) or False

      .. warning:: Use this option only when your evaluation function is slow, se you
                   will get a good tradeoff between the process communication speed and the
                   parallel evaluation.

      .. versionadded:: 0.6
         The `setMultiProcessing` method.

      """
      self.multiProcessing = flag
   
   def setMinimax(self, minimax):
      """ Sets the population minimax

      Example:
         >>> pop.setMinimax(Consts.minimaxType["maximize"])
   
      :param minimax: the minimax type

      """
      self.minimax = minimax

   def __repr__(self):
      """ Returns the string representation of the population """
      ret =  "- GPopulation\n"
      ret += "\tPopulation Size:\t %d\n" % (self.popSize,)
      ret += "\tSort Type:\t\t %s\n" % (Consts.sortType.keys()[Consts.sortType.values().index(self.sortType)].capitalize(),)
      ret += "\tMinimax Type:\t\t %s\n" % (Consts.minimaxType.keys()[Consts.minimaxType.values().index(self.minimax)].capitalize(),)
      for slot in self.allSlots:
         ret+= "\t" + slot.__repr__()
      ret+="\n"
      ret+= self.stats.__repr__()
      return ret

   def __len__(self):
      """ Return the length of population """
      return len(self.internalPop)
      
   def __getitem__(self, key):
      """ Returns the specified individual from population """
      return self.internalPop[key]

   def __iter__(self):
      """ Returns the iterator of the population """
      return iter(self.internalPop)

   def __setitem__(self, key, value):
      """ Set an individual of population """
      self.internalPop[key] = value
      self.clearFlags()

   def clearFlags(self):
      """ Clear the sorted and statted internal flags """
      self.sorted = False
      self.statted = False

   def getStatistics(self):
      """ Return a Statistics class for statistics

      :rtype: the :class:`Statistics.Statistics` instance

      """
      self.statistics()
      return self.stats      

   def statistics(self):
      """ Do statistical analysis of population and set 'statted' to True """
      if self.statted: return
      logging.debug("Running statistical calc.")
      raw_sum = 0
      fit_sum = 0

      len_pop = len(self)
      for ind in xrange(len_pop):
         raw_sum += self[ind].score
         fit_sum += self[ind].fitness

      self.stats["rawMax"] = max(self, key=Util.key_raw_score).score
      self.stats["rawMin"] = min(self, key=Util.key_raw_score).score
      self.stats["rawAve"] = raw_sum / float(len_pop)
      self.stats["rawTot"] = raw_sum
      self.stats["fitTot"] = fit_sum
      
      tmpvar = 0.0
      for ind in xrange(len_pop):
         s = self[ind].score - self.stats["rawAve"]
         s*= s
         tmpvar += s

      tmpvar/= float((len(self) - 1))
      self.stats["rawDev"] = math_sqrt(tmpvar)
      self.stats["rawVar"] = tmpvar

      self.statted = True

   def bestFitness(self, index=0):
      """ Return the best scaled fitness individual of population

      :param index: the *index* best individual
      :rtype: the individual

      """
      self.sort()
      return self.internalPop[index]

   def bestRaw(self, index=0):
      """ Return the best raw score individual of population

      :param index: the *index* best raw individual
      :rtype: the individual

      .. versionadded:: 0.6
         The parameter `index`.
      
      """
      if self.sortType == Consts.sortType["raw"]:
         return self.internalPop[index]
      else:
         self.sort()
         return self.internalPopRaw[index]

   def sort(self):
      """ Sort the population """
      if self.sorted: return
      rev = (self.minimax == Consts.minimaxType["maximize"])

      if self.sortType == Consts.sortType["raw"]:
         self.internalPop.sort(cmp=Util.cmp_individual_raw, reverse=rev)
      else:
         self.scale()
         self.internalPop.sort(cmp=Util.cmp_individual_scaled, reverse=rev)
         self.internalPopRaw = self.internalPop[:]
         self.internalPopRaw.sort(cmp=Util.cmp_individual_raw, reverse=rev)

      self.sorted = True

   def setPopulationSize(self, size):
      """ Set the population size

      :param size: the population size

      """
      self.popSize = size

   def setSortType(self, sort_type):
      """ Sets the sort type

      Example:
         >>> pop.setSortType(Consts.sortType["scaled"])

      :param sort_type: the Sort Type

      """
      self.sortType = sort_type

   def create(self, **args):
      """ Clone the example genome to fill the population """
      self.clear()
      self.minimax = args["minimax"]
      self.internalPop = [self.oneSelfGenome.clone() for i in xrange(self.popSize)]
      self.clearFlags()

   def initialize(self):
      """ Initialize all individuals of population,
      this calls the initialize() of individuals """
      for gen in self.internalPop:
         gen.initialize()
      self.clearFlags()

   def evaluate(self, **args):
      """ Evaluate all individuals in population, calls the evaluate() method of individuals
   
      :param args: this params are passed to the evaluation function

      """

      # We have multiprocessing
      if self.multiProcessing and MULTI_PROCESSING:
         pop_len = len(self)
         q = Queue()
         p1 = Process(target=async_eval, args=(self.internalPop[pop_len/2:], q)).start()
         p2 = Process(target=async_eval, args=(self.internalPop[:pop_len/2], q)).start()
         half1, half2 = q.get(), q.get()

         self.internalPop = half1 + half2

      else:
         for ind in self.internalPop:
            ind.evaluate(**args)

      self.clearFlags()

   def scale(self, **args):
      """ Scale the population using the scaling method

      :param args: this parameter is passed to the scale method

      """
      for it in self.scaleMethod.applyFunctions(self, **args):
         pass

      fit_sum = 0
      for ind in xrange(len(self)):
         fit_sum += self[ind].fitness

      self.stats["fitMax"] = max(self, key=Util.key_fitness_score).fitness
      self.stats["fitMin"] = min(self, key=Util.key_fitness_score).fitness
      self.stats["fitAve"] = fit_sum / float(len(self))

      self.sorted = False

   def printStats(self):
      """ Print statistics of the current population """
      message = ""
      if self.sortType == Consts.sortType["scaled"]:
         message =  "Max/Min/Avg Fitness(Raw) [%.2f(%.2f)/%.2f(%.2f)/%.2f(%.2f)]" % (self.stats["fitMax"], self.stats["rawMax"], self.stats["fitMin"], self.stats["rawMin"], self.stats["fitAve"], self.stats["rawAve"])
      else:
         message = "Max/Min/Avg Raw [%.2f/%.2f/%.2f]" % (self.stats["rawMax"], self.stats["rawMin"], self.stats["rawAve"])
      logging.info(message)
      print message
      return message

   def copy(self, pop):
      """ Copy current population to 'pop'

      :param pop: the destination population

      .. warning:: this method do not copy the individuals, only the population logic

      """
      pop.popSize = self.popSize
      pop.sortType = self.sortType
      pop.minimax = self.minimax
      pop.scaleMethod = self.scaleMethod
      pop.internalParams = self.internalParams.copy()
      pop.multiProcessing = self.multiProcessing
   
   def clear(self):
      """ Remove all individuals from population """
      del self.internalPop[:]
      del self.internalPopRaw[:]
      self.clearFlags()
      
   def clone(self):
      """ Return a brand-new cloned population """
      newpop = GPopulation(self.oneSelfGenome.clone())
      self.copy(newpop)
      return newpop
      

