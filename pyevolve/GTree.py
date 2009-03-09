"""

:mod:`GTree` -- the tree chromosome
=============================================================

This is the rooted tree representation, this chromosome representation
can carry any data-type.

Default Parameters
-------------------------------------------------------------

*Initializator*

  :func:`Initializators.GTreeInitializatorInteger`

   The Integer Initializator for GTree

*Mutator*
   
   :func:`Mutators.GTreeMutatorIntegerRange`

   The Integer Range mutator for GTree

*Crossover*

   :func:`Crossovers.GTreeCrossoverSinglePointStrict`

   The Strict Single Point crossover for GTree

.. versionadded:: 0.6
   The *GTree* module.

Classes
-------------------------------------------------------------
"""
import copy
from random import randint as rand_randint, choice as rand_choice
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

#################################
#    Tree Utility Functions     # 
#################################


def buildGTreeGrow(depth, value_callback, max_siblings, max_depth):
   """ Random generates a Tree structure using the value_callback
   for data generation and the method "Grow"

   :param depth: the initial depth, zero
   :param value_callback: the function which generates the random
                          values for nodes
   :param max_siblings: the maximum number of sisters of a node
   :param max_depth: the maximum depth of the tree   

   :rtype: the root node of created tree
   """

   random_value = value_callback()
   n = GTreeNode(random_value)

   if depth == max_depth: return n

   for i in xrange(rand_randint(0, abs(max_siblings))):
      child = buildGTreeGrow(depth+1, value_callback, max_siblings, max_depth)
      child.setParent(n)
      n.addChild(child)
   return n

def buildGTreeFull(depth, value_callback, max_siblings, max_depth):
   """ Random generates a Tree structure using the value_callback
   for data generation and the method "Full"

   :param depth: the initial depth, zero
   :param value_callback: the function which generates the random
                          values for nodes
   :param max_siblings: the maximum number of sisters of a node
   :param max_depth: the maximum depth of the tree   

   :rtype: the root node of created tree
   """

   random_value = value_callback()
   n = GTreeNode(random_value)

   if depth == max_depth: return n

   if max_siblings < 0: range_val = abs(max_siblings)
   else:                range_val = rand_randint(1, abs(max_siblings))
 
   for i in xrange(range_val):
      child = buildTreeFull(depth+1, value_callback, max_siblings, max_depth)
      child.setParent(n)
      n.addChild(child)
   return n


##################################################################################


class GTreeNodeGP(GTreeNodeBase):
   def __init__(self, data, node_type=0, parent=None):
      GTreeNodeBase.__init__(self, parent)
      self.node_type = node_type
      self.node_data = data

   def __repr__(self):
      str_repr  = GTreeNodeBase.__repr__(self)
      node_type_str = Consts.nodeType.keys()[self.node_type]
      str_repr += " - [%s][%s]" % (self.node_data, node_type_str)
      return str_repr     

   def setData(self, data):
      self.node_data = data

   def getData(self):
      return self.node_data

   def setType(self, node_type):
      self.node_type = node_type

   def getType(self):
      return self.node_type

   def newNode(self, data):
      node = GTreeNodeGP(data, self)
      self.addChild(node)
      return node

   def swapNodeData(self, node):
      tmp_data = self.node_data
      tmp_type = self.node_type
      self.setData(node.getData())
      self.setType(node.getType())
      node.setData(tmp_data)
      node.setType(tmp_type)


class GTreeGP(GenomeBase, GTreeBase):

   def __init__(self, root_node=None):
      GenomeBase.__init__(self)
      GTreeBase.__init__(self, root_node)
      self.initializator.set(Consts.CDefGTreeGPInit)
      self.mutator.set(Consts.CDefGGTreeGPMutator)
      self.crossover.set(Consts.CDefGTreeGPCrossover)

   def __repr__(self):
      """ Return a string representation of Genome """
      ret  = GenomeBase.__repr__(self)
      ret += GTreeBase.__repr__(self)
      return ret

   def getSExpression(self, start_node=None):
      """ Returns a tree-formated string of the tree. This
      method is used by the __repr__ method of the tree
      
      :rtype: a string representing the tree
      """
      str_buff = ""
      if start_node is None:
         start_node = self.getRoot()
         str_buff += "%s " % start_node.getData()

      is_leaf = start_node.isLeaf()
      if not is_leaf:
         str_buff += "( "

      for child_node in start_node.getChilds():
         str_buff += "%s " % child_node.getData()
         str_buff += self.getExpression(child_node)

      if not is_leaf:
         str_buff += ") "
      return str_buff

   def getNExpression(self, start_node=None):
      """ Returns a tree-formated string of the tree. This
      method is used by the __repr__ method of the tree
      
      :rtype: a string representing the tree
      """
      str_buff = ""
      if start_node is None:
         start_node = self.getRoot()

      is_leaf = start_node.isLeaf()

      left  = None
      right = None

      if not is_leaf:
         childs = start_node.getChilds()
         left  = childs[0]
         right = childs[1]

      if not is_leaf:
         str_buff += "("

      if left is not None:
         str_buff += self.getNExpression(left)
      
      str_buff += start_node.getData()

      if right is not None:
         str_buff += self.getNExpression(right)

      if not is_leaf:
         str_buff += ")"

      return str_buff

   def clone(self):
      """ Return a new instance of the genome"""
      return copy.deepcopy(self)

def buildGTreeGPGrow(depth, max_depth):
   if depth == max_depth:
      random_terminal = rand_choice(Consts.TERMINALS)
      n = GTreeNodeGP(random_terminal, Consts.nodeType["TERMINAL"])
      return n
   else:
      fchoice = rand_choice([Consts.FUNCTIONS, Consts.TERMINALS])
      random_node = rand_choice(fchoice)

      if random_node in Consts.TERMINALS:
         n = GTreeNodeGP(random_node, Consts.nodeType["TERMINAL"])
      else:
         n = GTreeNodeGP(random_node, Consts.nodeType["NONTERMINAL"])

   if n.getType() == Consts.nodeType["NONTERMINAL"]:
      for i in xrange(Consts.FUNCTIONS_OP[n.getData()]):
         child = buildGTreeGPGrow(depth+1, max_depth)
         child.setParent(n)
         n.addChild(child)

   return n

def buildGTreeGPFull(depth, max_depth):
   if depth == max_depth:
      random_terminal = rand_choice(Consts.TERMINALS)
      n = GTreeNodeGP(random_terminal, Consts.nodeType["TERMINAL"])
      return n
   else:
      random_oper = rand_choice(Consts.FUNCTIONS)

      if random_oper in Consts.TERMINALS:
         n = GTreeNodeGP(random_oper, Consts.nodeType["TERMINAL"])
      else:
         n = GTreeNodeGP(random_oper, Consts.nodeType["NONTERMINAL"])

   if n.getType() == Consts.nodeType["NONTERMINAL"]:
      for i in xrange(Consts.FUNCTIONS_OP[n.getData()]):
         child = buildGTreeGPFull(depth+1, max_depth)
         child.setParent(n)
         n.addChild(child)

   return n
