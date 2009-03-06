"""

:mod:`Crossovers` -- crossover methdos module
=====================================================================

In this module we have the genetic operators of crossover (or recombination) for each chromosome representation.

"""

from random import randint as rand_randint, choice as rand_choice
import Util
import Consts

#############################
##     1D Binary String    ##
#############################

def G1DBinaryStringXSinglePoint(genome, **args):
   """ The crossover of 1D Binary String, Single Point

   .. warning:: You can't use this crossover method for binary strings with length of 1.

   """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]

   if len(gMom) == 1:
      Util.raiseException("The Binary String have one element, can't use the Single Point Crossover method !", TypeError)

   cut = rand_randint(1, len(gMom)-1)

   if args["count"] >= 1:
      sister = gMom.clone()
      sister.resetStats()
      sister[cut:] = gDad[cut:]

   if args["count"] == 2:
      brother = gDad.clone()
      brother.resetStats()
      brother[cut:] = gMom[cut:]

   return (sister, brother)

def G1DBinaryStringXTwoPoint(genome, **args):
   """ The 1D Binary String crossover, Two Point

   .. warning:: You can't use this crossover method for binary strings with length of 1.

   """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]
   
   if len(gMom) == 1:
      Util.raiseException("The Binary String have one element, can't use the Two Point Crossover method !", TypeError)

   cuts = [rand_randint(1, len(gMom)-1), rand_randint(1, len(gMom)-1)]

   if cuts[0] > cuts[1]:
      Util.listSwapElement(cuts, 0, 1)

   if args["count"] >= 1:
      sister = gMom.clone()
      sister.resetStats()
      sister[cuts[0]:cuts[1]] = gDad[cuts[0]:cuts[1]]

   if args["count"] == 2:
      brother = gDad.clone()
      brother.resetStats()
      brother[cuts[0]:cuts[1]] = gMom[cuts[0]:cuts[1]]

   return (sister, brother)

def G1DBinaryStringXUniform(genome, **args):
   """ The G1DList Uniform Crossover """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]

   sister = gMom.clone()
   brother = gDad.clone()
   sister.resetStats()
   brother.resetStats()

   for i in xrange(len(gMom)):
      if Util.randomFlipCoin(Consts.CDefG1DBinaryStringUniformProb):
         temp = sister[i]
         sister[i] = brother[i]
         brother[i] = temp
            
   return (sister, brother)

####################
##     1D List    ##
####################
     
def G1DListCrossoverSinglePoint(genome, **args):
   """ The crossover of G1DList, Single Point

   .. warning:: You can't use this crossover method for lists with just one element.

   """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]
   
   if len(gMom) == 1:
      Util.raiseException("The 1D List have one element, can't use the Single Point Crossover method !", TypeError)
      
   cut = rand_randint(1, len(gMom)-1)

   if args["count"] >= 1:
      sister = gMom.clone()
      sister.resetStats()
      sister[cut:] = gDad[cut:]

   if args["count"] == 2:
      brother = gDad.clone()
      brother.resetStats()
      brother[cut:] = gMom[cut:]

   return (sister, brother)

def G1DListCrossoverTwoPoint(genome, **args):
   """ The G1DList crossover, Two Point

   .. warning:: You can't use this crossover method for lists with just one element.

   """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]
   
   if len(gMom) == 1:
      Util.raiseException("The 1D List have one element, can't use the Two Point Crossover method !", TypeError)

   cuts = [rand_randint(1, len(gMom)-1), rand_randint(1, len(gMom)-1)]

   if cuts[0] > cuts[1]:
      Util.listSwapElement(cuts, 0, 1)

   if args["count"] >= 1:
      sister = gMom.clone()
      sister.resetStats()
      sister[cuts[0]:cuts[1]] = gDad[cuts[0]:cuts[1]]

   if args["count"] == 2:
      brother = gDad.clone()
      brother.resetStats()
      brother[cuts[0]:cuts[1]] = gMom[cuts[0]:cuts[1]]

   return (sister, brother)

def G1DListCrossoverUniform(genome, **args):
   """ The G1DList Uniform Crossover """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]

   sister = gMom.clone()
   brother = gDad.clone()
   sister.resetStats()
   brother.resetStats()

   for i in xrange(len(gMom)):
      if Util.randomFlipCoin(Consts.CDefG1DListCrossUniformProb):
         temp = sister[i]
         sister[i] = brother[i]
         brother[i] = temp
            
   return (sister, brother)

def G1DListCrossoverOX(genome, **args):
   """ The OX Crossover of G1DList """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]
   listSize = len(gMom)

   c1, c2 = [rand_randint(1, len(gMom)-1), rand_randint(1, len(gMom)-1)]

   while c1 == c2:
      c2 = rand_randint(1, len(gMom)-1)

   if c1 > c2:
      h = c1
      c1 = c2
      c2 = h

   if args["count"] >= 1:
      sister = gMom.clone()
      sister.resetStats()
      P1 = [ c for c in gMom[c2:] + gMom[:c2] if c not in gDad[c1:c2] ]
      sister.genomeList = P1[listSize - c2:] + gDad[c1:c2] + P1[:listSize-c2]
    
   if args["count"] == 2:
      brother = gDad.clone()
      brother.resetStats()
      P2 = [ c for c in gDad[c2:] + gDad[:c2] if c not in gMom[c1:c2] ]
      brother.genomeList = P2[listSize - c2:] + gMom[c1:c2] + P2[:listSize-c2]

   assert listSize == len(sister)

   return (sister, brother)


####################
##     2D List    ##
####################

def G2DListCrossoverUniform(genome, **args):
   """ The G2DList Uniform Crossover """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]

   sister = gMom.clone()
   brother = gDad.clone()
   sister.resetStats()
   brother.resetStats()
   
   h, w = gMom.getSize()
   
   for i in xrange(h):
      for j in xrange(w):
         if Util.randomFlipCoin(Consts.CDefG2DListCrossUniformProb):
            temp = sister.getItem(i, j)
            sister.setItem(i, j, brother.getItem(i, j))
            brother.setItem(i, j, temp)

   return (sister, brother)


def G2DListCrossoverSingleVPoint(genome, **args):
   """ The crossover of G2DList, Single Vertical Point """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]

   cut = rand_randint(1, gMom.getWidth()-1)

   if args["count"] >= 1:
      sister = gMom.clone()
      sister.resetStats()
      for i in xrange(sister.getHeight()):
         sister[i][cut:] = gDad[i][cut:]

   if args["count"] == 2:
      brother = gDad.clone()
      brother.resetStats()
      for i in xrange(brother.getHeight()):
         brother[i][cut:] = gMom[i][cut:]

   return (sister, brother)

def G2DListCrossoverSingleHPoint(genome, **args):
   """ The crossover of G2DList, Single Horizontal Point """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]

   cut = rand_randint(1, gMom.getHeight()-1)

   if args["count"] >= 1:
      sister = gMom.clone()
      sister.resetStats()
      for i in xrange(cut, sister.getHeight()):
         sister[i][:] = gDad[i][:]

   if args["count"] == 2:
      brother = gDad.clone()
      brother.resetStats()
      for i in xrange(brother.getHeight()):
         brother[i][:] = gMom[i][:]

   return (sister, brother)


#############################
##     2D Binary String    ##
#############################


def G2DBinaryStringXUniform(genome, **args):
   """ The G2DBinaryString Uniform Crossover
   
   .. versionadded:: 0.6
      The *G2DBinaryStringXUniform* function
   """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]

   sister = gMom.clone()
   brother = gDad.clone()
   sister.resetStats()
   brother.resetStats()
   
   h, w = gMom.getSize()
   
   for i in xrange(h):
      for j in xrange(w):
         if Util.randomFlipCoin(Consts.CDefG2DBinaryStringUniformProb):
            temp = sister.getItem(i, j)
            sister.setItem(i, j, brother.getItem(i, j))
            brother.setItem(i, j, temp)

   return (sister, brother)


def G2DBinaryStringXSingleVPoint(genome, **args):
   """ The crossover of G2DBinaryString, Single Vertical Point
   
   .. versionadded:: 0.6
      The *G2DBinaryStringXSingleVPoint* function
   """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]

   cut = rand_randint(1, gMom.getWidth()-1)

   if args["count"] >= 1:
      sister = gMom.clone()
      sister.resetStats()
      for i in xrange(sister.getHeight()):
         sister[i][cut:] = gDad[i][cut:]

   if args["count"] == 2:
      brother = gDad.clone()
      brother.resetStats()
      for i in xrange(brother.getHeight()):
         brother[i][cut:] = gMom[i][cut:]

   return (sister, brother)

def G2DBinaryStringXSingleHPoint(genome, **args):
   """ The crossover of G2DBinaryString, Single Horizontal Point
   
   .. versionadded:: 0.6
      The *G2DBinaryStringXSingleHPoint* function
  
   """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]

   cut = rand_randint(1, gMom.getHeight()-1)

   if args["count"] >= 1:
      sister = gMom.clone()
      sister.resetStats()
      for i in xrange(cut, sister.getHeight()):
         sister[i][:] = gDad[i][:]

   if args["count"] == 2:
      brother = gDad.clone()
      brother.resetStats()
      for i in xrange(brother.getHeight()):
         brother[i][:] = gMom[i][:]

   return (sister, brother)

#############################
##          Tree           ##
#############################


def GTreeCrossoverSinglePoint(genome, **args):
   """ The crossover of Tree, Single Point """
   sister = None
   brother = None
   gMom = args["mom"].clone()
   gDad = args["dad"].clone()

   gMom.resetStats()
   gDad.resetStats()

   node_mom_stack = []
   all_mom_nodes  = []
   node_mom_tmp   = None

   node_dad_stack = []
   all_dad_nodes  = []
   node_dad_tmp   = None

   node_mom_stack.append(gMom.getRoot())
   node_dad_stack.append(gDad.getRoot())

   while (len(node_mom_stack) > 0) and  (len(node_dad_stack) > 0):
      node_mom_tmp = node_mom_stack.pop()
      node_dad_tmp = node_dad_stack.pop()

      if node_mom_tmp != gMom.getRoot():
         all_mom_nodes.append(node_mom_tmp)
         all_dad_nodes.append(node_dad_tmp)

      node_mom_stack.extend(node_mom_tmp.getChilds())
      node_dad_stack.extend(node_dad_tmp.getChilds())

   if len(all_mom_nodes)==0 or len(all_dad_nodes)==0:
      return (gMom, gDad)

   if len(all_dad_nodes) == 1: nodeDad = all_dad_nodes[0]
   else: nodeDad = rand_choice(all_dad_nodes)

   if len(all_mom_nodes) == 1: nodeMom = all_mom_nodes[0]
   else: nodeMom = rand_choice(all_mom_nodes)

   nodeMom_parent = nodeMom.getParent()
   nodeDad_parent = nodeDad.getParent()

   # Sister
   if args["count"] >= 1:
      sister = gMom
      nodeDad.setParent(nodeMom_parent)
      nodeMom_parent.replaceChild(nodeMom, nodeDad)
      sister.processNodes()

   # Brother
   if args["count"] == 2:
      brother = gDad
      nodeMom.setParent(nodeDad_parent)
      nodeDad_parent.replaceChild(nodeDad, nodeMom)
      brother.processNodes()

   return (sister, brother)

def GTreeCrossoverSinglePointStrict(genome, **args):
   """ The crossover of Tree, Strict Single Point

   ..note:: This crossover method creates offspring with restriction of the
            *max_depth* parameter.
   
   Accepts the *max_attempt* parameter and *max_depth* (required).
   
   """
   sister = None
   brother = None

   gMom = args["mom"].clone()
   gDad = args["dad"].clone()

   #gMom.processNodes()
   #gDad.processNodes()

   gMom.resetStats()
   gDad.resetStats()

   max_depth = gMom.getParam("max_depth", None)
   max_attempt = gMom.getParam("max_attempt", 10)

   if max_depth is None:
      Util.raiseException("You must specify the max_depth genome parameter !", ValueError)
      
   if max_depth < 0:
      Util.raiseException("The max_depth must be >= 1, if you want to use GTreeCrossoverSinglePointStrict crossover !", ValueError)

   momRandom = None
   dadRandom = None

   for i in xrange(max_attempt):
      momRandom = gMom.getRandomNode()
      dadRandom = gDad.getRandomNode()

      # Optimize here
      mH = gMom.getNodeHeight(momRandom)
      dH = gDad.getNodeHeight(dadRandom)

      mD = gMom.getNodeDepth(momRandom)
      dD = gDad.getNodeDepth(dadRandom)

      if (mH==0) and (dH==0): continue

      if (dD+mH <= max_depth) and (mD+dH <= max_depth):
         break

   if i==(max_attempt-1):
      assert gMom.getHeight() <= max_depth
      return (gMom, gDad)
   else:
      nodeMom, nodeDad = momRandom, dadRandom

   nodeMom_parent = nodeMom.getParent()
   nodeDad_parent = nodeDad.getParent()

   # Sister
   if args["count"] >= 1:
      sister = gMom
      nodeDad.setParent(nodeMom_parent)

      if nodeMom_parent is None:
         sister.setRoot(nodeDad)
      else:
         nodeMom_parent.replaceChild(nodeMom, nodeDad)
      sister.processNodes()
      assert sister.getHeight() <= max_depth

   # Brother
   if args["count"] == 2:
      brother = gDad
      nodeMom.setParent(nodeDad_parent)

      if nodeDad_parent is None:
         brother.setRoot(nodeMom)
      else:
         nodeDad_parent.replaceChild(nodeDad, nodeMom)
      brother.processNodes()
      assert brother.getHeight() <= max_depth

   return (sister, brother)

