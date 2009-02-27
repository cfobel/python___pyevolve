"""

:mod:`GTree` -- the tree chromosome
=============================================================

This is the rooted tree representation, this chromosome representation
can carry any data-type.

Default Parameters
-------------------------------------------------------------

*Initializator*

  :func:`Initializators.GTreeInitInteger`

   The Integer Initializator for GTree

*Mutator*
   TODO

*Crossover*
   TODO

.. versionadded:: 0.6
   The *GTree* module.

Classes
-------------------------------------------------------------
"""
import copy
from random import randint as rand_randint
from GenomeBase import GenomeBase, GTreeBase, GTreeNodeBase
import Consts

class GTree(GenomeBase, GTreeBase):
   """ The GTree class - The tree chromosome representation

   :param root_node: the root node of the tree
   """
   
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

   def __init__(self, root_node=None):
      GenomeBase.__init__(self)
      GTreeBase.__init__(self, root_node)
      self.initializator.set(Consts.CDefGTreeInit)
      self.mutator.set(Consts.CDefGGTreeMutator)
      self.crossover.set(Consts.CDefGTreeCrossover)

   def __repr__(self):
      """ Return a string representation of Genome """
      ret  = GenomeBase.__repr__(self)
      ret += GTreeBase.__repr__(self)
      return ret

   def clone(self):
      """ Return a new instance of the genome"""
      return copy.deepcopy(self)

class GTreeNode(GTreeNodeBase):
   """ The GTreeNode class - The node representation

   :param data: the root node of the tree
   :param parent: the parent node, if root, this
                  must be *None*
   """

   def __init__(self, data, parent=None):
      GTreeNodeBase.__init__(self, parent)
      self.node_data = data

   def __repr__(self):
      str_repr  = GTreeNodeBase.__repr__(self)
      str_repr += " - [%s]" % self.node_data
      return str_repr     

   def setData(self, data):
      """ Sets the data of the node

      :param data: the data of the node
      """
      self.node_data = data

   def getData(self):
      """ Return the data of the node

      :rtype: the data of the node
      """
      return self.node_data

   def newNode(self, data):
      """ Created a new child node

      :param data: the data of the new created node
      """
      node = GTreeNode(data, self)
      self.addChild(node)
      return node

   def swapNodeData(self, node):
      """ Swaps the node data with another node
      
      :param node: the node to do the data swap
      """
      tmp_data = self.node_data
      self.setData(node.getData())
      node.setData(tmp_data)

#############################
#     Utility Functions     # 
#############################


def buildTreeGrow(depth, value_callback, max_sister, max_depth):
   """ Random generates a Tree structure using the value_callback
   for data generation and the method "Grow"

   :param depth: the initial depth, zero
   :param value_callback: the function which generates the random
                          values for nodes
   :param max_sister: the maximum number of sisters of a node
   :param max_depth: the maximum depth of the tree   

   :rtype: the root node of created tree
   """

   random_value = value_callback()
   n = GTreeNode(random_value)

   if depth == max_depth: return n

   for i in xrange(rand_randint(0, abs(max_sister))):
      child = buildTreeGrow(depth+1, value_callback, max_sister, max_depth)
      child.setParent(n)
      n.addChild(child)
   return n


def buildTreeFull(depth, value_callback, max_sister, max_depth):
   """ Random generates a Tree structure using the value_callback
   for data generation and the method "Full"

   :param depth: the initial depth, zero
   :param value_callback: the function which generates the random
                          values for nodes
   :param max_sister: the maximum number of sisters of a node
   :param max_depth: the maximum depth of the tree   

   :rtype: the root node of created tree
   """

   random_value = value_callback()
   n = GTreeNode(random_value)

   if depth == max_depth: return n

   if max_sister < 0: range_val = abs(max_sister)
   else:              range_val = rand_randint(1, abs(max_sister))

   for i in xrange(range_val):
      child = buildTreeFull(depth+1, value_callback, max_sister, max_depth)
      child.setParent(n)
      n.addChild(child)
   return n
