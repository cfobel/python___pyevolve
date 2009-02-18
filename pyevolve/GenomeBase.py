"""

:mod:`GenomeBase` -- the genomes base module
================================================================

This module have the class which every representation extends,
if you are planning to create a new representation, you must
take a inside look into this module.

"""
from FunctionSlot import FunctionSlot
import Util

class GenomeBase:
   """ GenomeBase Class - The base of all chromosome representation """

   evaluator = None
   """ This is the :term:`evaluation function` slot, you can add
   a function with the *set* method: ::

      genome.evaluator.set(eval_func)
   """

   initializator = None
   """ This is the initialization function of the genome, you
   can change the default initializator using the function slot: ::

      genome.initializator.set(Initializators.G1DListInitializatorAllele)

   In this example, the initializator :func:`Initializators.G1DListInitializatorAllele`
   will be used to create the initial population.
   """

   mutator = None
   """ This is the mutator function slot, you can change the default
   mutator using the slot *set* function: ::

      genome.mutator.set(Mutators.G1DListMutatorSwap)

   """

   crossover = None
   """ This is the reproduction function slot, the crossover. You
   can change the default crossover method using: ::

      genome.crossover.set(Crossovers.G1DListCrossoverUniform)
   """


   def __init__(self):
      """Genome Constructor"""
      self.evaluator = FunctionSlot("Evaluator")
      self.initializator = FunctionSlot("Initializator")
      self.mutator = FunctionSlot("Mutator")
      self.crossover = FunctionSlot("Crossover")
 
      self.allSlots = [ self.evaluator, self.initializator,
                      self.mutator, self.crossover ]
      
      self.internalParams = {}
      self.score = 0.0
      self.fitness = 0.0

   def getRawScore(self):
      """ Get the Raw Score of the genome

      :rtype: genome raw score

      """
      return self.score

   def getFitnessScore(self):
      """ Get the Fitness Score of the genome

      :rtype: genome fitness score

      """
      return self.fitness

   def __repr__(self):
      """String representation of Genome"""
      ret = "- GenomeBase\n"
      ret+= "\tScore:\t\t\t %.6f\n" % (self.score,)
      ret+= "\tFitness:\t\t %.6f\n\n" % (self.fitness,)
      #ret+= "\tInit Params:\t\t %s\n\n" % (self.internalParams,)

      for slot in self.allSlots:
         ret+= "\t" + slot.__repr__()
      ret+="\n"

      return ret

   def setParams(self, **args):
      """ Set the internal params

      Example:
         >>> genome.setParams(rangemin=0, rangemax=100, gauss_mu=0, gauss_sigma=1)

      :param args: this params will saved in every chromosome for genetic op. use

      """
      self.internalParams.update(args)
   
   def getParam(self, key, nvl=None):
      """ Gets an internal parameter

      Example:
         >>> genome.getParam("rangemax")
         100

      :param key: the key of param
      :param nvl: if the key doesn't exist, the nvl will be returned

      """
      return self.internalParams.get(key, nvl)
      
   def resetStats(self):
      """ Clear score and fitness of genome """
      self.score = 0.0
      self.fitness = 0.0
      
   def evaluate(self, **args):
      """ Called to evaluate genome

      :param args: this parameters will be passes to the evaluator

      """
      self.resetStats()
      for it in self.evaluator.applyFunctions(self, **args):
         self.score += it

   def initialize(self, **args):
      """ Called to initialize genome

      :param args: this parameters will be passed to the initializator

      """
      for it in self.initializator.applyFunctions(self, **args):
         pass

   def mutate(self, **args):
      """ Called to mutate the genome

      :param args: this parameters will be passed to the mutator

      """
      nmuts = 0 
      for it in self.mutator.applyFunctions(self, **args):
         nmuts+=it
      return nmuts

   def copy(self, g):
      """ Copy the current GenomeBase to 'g'

      :param g: the destination genome      

      .. note:: If you are planning to create a new chromosome representation, you
                **must** implement this method on your class.
      """
      g.score = self.score
      g.fitness = self.fitness
      g.evaluator = self.evaluator
      g.initializator = self.initializator
      g.mutator = self.mutator
      g.crossover = self.crossover
      g.allSlots = self.allSlots[:]
      g.internalParams = self.internalParams.copy()
      
   def clone(self):
      """ Clone this GenomeBase

      :rtype: the clone genome   

      .. note:: If you are planning to create a new chromosome representation, you
                **must** implement this method on your class.
      """
      newcopy = GenomeBase()
      self.copy(newcopy)
      return newcopy
   
class G1DBase:
   """ G1DBase Class - The base class for 1D chromosomes
   
   :param size: the 1D list size

   .. versionadded:: 0.6
      Added te *G1DBase* class
   """

   def __init__(self, size):
      self.genomeSize = size
      self.genomeList = []

   def __iadd__(self, item):
      """ To add more items using the += operator """
      self.genomeList.append(item)
      return self

   def __eq__(self, other):
      """ Compares one chromosome with another """
      cond1 = (self.genomeList == other.genomeList)
      cond2 = (self.genomeSize   == other.genomeSize)
      return True if cond1 and cond2 else False
   
   def __contains__(self, value):
      """ Used on: *value in genome* """
      return value in self.genomeList

   def __getslice__(self, a, b):
      """ Return the sliced part of chromosome """
      return self.genomeList[a:b]

   def __getitem__(self, key):
      """ Return the specified gene of List """
      return self.genomeList[key]

   def __setitem__(self, key, value):
      """ Set the specified value for an gene of List """
      self.genomeList[key] = value

   def __iter__(self):
      """ Iterator support to the list """
      return iter(self.genomeList)
   
   def __len__(self):
      """ Return the size of the List """
      return len(self.genomeList)

   def getListSize(self):
      """ Returns the list supposed size

      .. warning:: this is different from what the len(obj) returns
      """
      return self.genomeSize

   def resumeString(self):
      """ Returns a resumed string representation of the Genome """
      return str(self.genomeList)

   def append(self, value):
      """ Appends an item to the end of the list
      
      Example:
         >>> genome.append(44)

      :param value: value to be added
      
      """
      self.genomeList.append(value)

   def remove(self, value):
      """ Removes an item from the list
      
      Example:
         >>> genome.remove(44)

      :param value: value to be added
      
      """
      self.genomeList.remove(value)

   def clearList(self):
      """ Remove all genes from Genome """
      del self.genomeList[:]
   
   def copy(self, g):
      """ Copy genome to 'g'
      
      Example:
         >>> genome_origin.copy(genome_destination)
      
      :param g: the destination instance

      """
      g.genomeSize = self.genomeSize
      g.genomeList = self.genomeList[:]

   