"""

:mod:`Initializators` -- initialization methods module
===================================================================

In this module we have the genetic operators of initialization for each
chromosome representation, the most part of initialization is done by
choosing random data.

.. note:: In Pyevolve, the Initializator defines the data type that will
          be used on the chromosome, for example, the :func:`G1DListInitializatorInteger`
          will initialize the G1DList with Integers.
          

"""

from random import randint as rand_randint, uniform as rand_uniform, choice as rand_choice
import Util

#############################
##     1D Binary String    ##
#############################

def G1DBinaryStringInitializator(genome, **args):
   """ 1D Binary String initializator """
   genome.genomeString = [ rand_choice((0,1)) for i in xrange(len(genome)) ]

#############################
##     2D Binary String    ##
#############################

def G2DBinaryStringInitializator(genome, **args):
   """ Integer initialization function of 2D Binary String
   
   .. versionadded:: 0.6
      The *G2DBinaryStringInitializator* function
   """
   genome.clearString()
   
   for i in xrange(genome.getHeight()):
      for j in xrange(genome.getWidth()):
         random_gene = rand_choice((0,1))
         genome.setItem(i, j, random_gene)


####################
##     1D List    ##
####################

def G1DListInitializatorAllele(genome, **args):
   """ Allele initialization function of G1DList

   To use this initializator, you must specify the *allele* genome parameter with the
   :class:`GAllele.GAlleles` instance.

   """

   allele = genome.getParam("allele", None)
   if allele is None:
      Util.raiseException("to use the G1DListInitializatorAllele, you must specify the 'allele' parameter")

   genome.genomeList = [ allele[i].getRandomAllele() for i in xrange(genome.listSize)  ]

def G1DListInitializatorInteger(genome, **args):
   """ Integer initialization function of G1DList

   This initializator accepts the *rangemin* and *rangemax* genome parameters.

   """
   range_min = genome.getParam("rangemin", 0)
   range_max = genome.getParam("rangemax", 100)

   genome.genomeList = [rand_randint(range_min, range_max) for i in xrange(genome.listSize)]

def G1DListInitializatorReal(genome, **args):
   """ Real initialization function of G1DList

   This initializator accepts the *rangemin* and *rangemax* genome parameters.

   """
   range_min = genome.getParam("rangemin", 0)
   range_max = genome.getParam("rangemax", 100)

   genome.genomeList = [rand_uniform(range_min, range_max) for i in xrange(genome.listSize)]


####################
##     2D List    ##
####################

def G2DListInitializatorInteger(genome, **args):
   """ Integer initialization function of G2DList

   This initializator accepts the *rangemin* and *rangemax* genome parameters.
   
   """
   genome.clearList()
   
   for i in xrange(genome.getHeight()):
      for j in xrange(genome.getWidth()):
         randomInteger = rand_randint(genome.getParam("rangemin", 0),
                                      genome.getParam("rangemax", 100))
         genome.setItem(i, j, randomInteger)


def G2DListInitializatorReal(genome, **args):
   """ Integer initialization function of G2DList

   This initializator accepts the *rangemin* and *rangemax* genome parameters.

   """
   genome.clearList()
   
   for i in xrange(genome.getHeight()):
      for j in xrange(genome.getWidth()):
         randomReal = rand_uniform(genome.getParam("rangemin", 0),
                                   genome.getParam("rangemax", 100))
         genome.setItem(i, j, randomReal)

def G2DListInitializatorAllele(genome, **args):
   """ Allele initialization function of G2DList

   To use this initializator, you must specify the *allele* genome parameter with the
   :class:`GAllele.GAlleles` instance.

   .. warning:: the :class:`GAllele.GAlleles` instance must have the homogeneous flag enabled

   """

   allele = genome.getParam("allele", None)
   if allele is None:
      Util.raiseException("to use the G2DListInitializatorAllele, you must specify the 'allele' parameter")

   if allele.homogeneous == False:
      Util.raiseException("to use the G2DListInitializatorAllele, the 'allele' must be homogeneous")

   genome.clearList()
   
   for i in xrange(genome.getHeight()):
      for j in xrange(genome.getWidth()):
         random_allele = allele[0].getRandomAllele()
         genome.setItem(i, j, random_allele)
