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
import Util

#################################
#             GTree             # 
#################################


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

   def copy(self, g):
      """ Copy the contents to the destination g
      
      :param g: the GTree genome destination
      """
      GenomeBase.copy(self, g)
      GTreeBase.copy(self, g)

   def clone(self):
      """ Return a new instance of the genome
      
      :rtype: new GTree instance
      """
      newcopy = GTree()
      self.copy(newcopy)
      newcopy.processNodes(True)
      return newcopy

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

   def copy(self, g):
      """ Copy the contents to the destination g
      
      :param g: the GTreeNode genome destination
      """
      GTreeNodeBase.copy(self, g)
      g.node_data = self.node_data

   def clone(self):
      """ Return a new instance of the genome
      
      :rtype: new GTree instance
      """
      newcopy = GTreeNode(None)
      self.copy(newcopy)
      return newcopy

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

#################################
#             GTree   GP        # 
#################################

class GTreeNodeGP(GTreeNodeBase):
   """ The GTreeNodeGP Class - The Genetic Programming Node representation
   
   :param data: the node data
   :param type: the node type
   :param parent: the node parent
   
   """
   def __init__(self, data, node_type=0, parent=None):
      GTreeNodeBase.__init__(self, parent)
      self.node_type = node_type
      self.node_data = data

   def __repr__(self):
      str_repr  = GTreeNodeBase.__repr__(self)
      node_type_str = Consts.nodeType.keys()[self.node_type]
      str_repr += " - [%s][%s]" % (self.node_data, node_type_str)
      return str_repr     

   def compare(self, other):
      """ Compare this node with other 
      
      :param other: the other GTreeNodeGP
      """
      if not isinstance(other, GTreeNodeGP):
         Util.raiseException("The other node used to compare is not a GTreeNodeGP class", TypeError)

      if other.node_type == self.node_type:
         if other.node_data == self.node_data:
            return 0
      return -1

   def setData(self, data):
      """Sets the node internal data
      
      :param data: the internal data
      """
      self.node_data = data

   def getData(self):
      """Gets the node internal data
      
      :rtype: the internal data
      """
      return self.node_data

   def setType(self, node_type):
      """Sets the node type 
      
      :param node_type: the node type is type of Consts.nodeType
      """
      self.node_type = node_type

   def getType(self):
      """Get the node type 
      
      :rtype: the node type is type of Consts.nodeType
      """
      return self.node_type

   def newNode(self, data):
      """Creates a new node and adds this
      node as children of current node

      :param data: the internal node data
      """
      node = GTreeNodeGP(data, self)
      self.addChild(node)
      return node

   def swapNodeData(self, node):
      """Swaps the node data and type with another node

      :param node: the node
      """
      tmp_data = self.node_data
      tmp_type = self.node_type
      self.setData(node.getData())
      self.setType(node.getType())
      node.setData(tmp_data)
      node.setType(tmp_type)

   def copy(self, g):
      """ Copy the contents to the destination g
      
      :param g: the GTreeNodeGP genome destination
      """
      GTreeNodeBase.copy(self, g)
      g.node_data = self.node_data
      g.node_type = self.node_type

   def clone(self):
      """ Return a new copy of the node

      :rtype: the new GTreeNodeGP instance
      """
      newcopy = GTreeNodeGP(None)
      self.copy(newcopy)
      return newcopy

class GTreeGP(GenomeBase, GTreeBase):
   """ The GTreeGP Class - The Genetic Programming Tree representation
   
   :param root_node: the Root node of the GP Tree
   """
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
      ret += "\n- GTreeGP\n"      
      ret += "\tExpression: %s\n" % self.getPreOrderExpression()
      return ret

   def writeDotGraph(self, graph, startNode=0):
      """ Write a graph to the pydot Graph instance
      
      :param graph: the pydot Graph instance
      :param startNode: used to plot more than one individual 
      """
      pydot = Util.importSpecial("pydot")
      graph.set_type("graph")
      count = startNode
      node_stack = []
      nodes_dict = {}
      tmp = None

      for i in xrange(len(self.nodes_list)):
         newnode = pydot.Node(str(count), style="filled")
         count += 1
         newnode.set_label(self.nodes_list[i].getData())
         nodes_dict.update({self.nodes_list[i]: newnode})
         if self.nodes_list[i].getType() == Consts.nodeType["TERMINAL"]:
            newnode.set_color("lightblue2")
         else:
            newnode.set_color("goldenrod2")

         graph.add_node(newnode)

      node_stack.append(self.getRoot())
      while len(node_stack) > 0:
         tmp = node_stack.pop()

         parent = tmp.getParent()
         if parent is not None:
            parent_node = nodes_dict[parent]
            child_node  = nodes_dict[tmp]
           
            newedge = pydot.Edge(parent_node, child_node)
            graph.add_edge(newedge)
   
         rev_childs = tmp.getChilds()[:]
         rev_childs.reverse()
         node_stack.extend(rev_childs)

      return count

   def getSExpression(self, start_node=None):
      """ Returns a tree-formated string (s-expression) of the tree.
      
      :rtype: a S-Expression representing the tree
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

   def getPreOrderExpression(self, start_node=None):
      """ Return the pre order expression string of the Tree, used
      to python *eval*.

      :rtype: the expression string
      """
      str_buff = ""

      if start_node is None:
         start_node = self.getRoot()

      node_data = start_node.getData()
      str_buff += node_data

      if not start_node.isLeaf():
         all_childs = start_node.getChilds()
         first_child = all_childs[0]
         str_buff += "(" + self.getPreOrderExpression(first_child)

         for index in xrange(1, len(all_childs)):
            child = all_childs[index]
            str_buff += ", " + self.getPreOrderExpression(child)
         str_buff += ")"
      
      return str_buff

   def getCompiledCode(self):
      """ Get the compiled code for the Tree expression
      
      :rtype: compiled python code
      """
      expr = self.getPreOrderExpression()
      return compile(expr, "<string>", "eval")

   def copy(self, g):
      """ Copy the contents to the destination g
      
      :param g: the GTreeGP genome destination
      """
      GenomeBase.copy(self, g)
      GTreeBase.copy(self, g)

   def clone(self):
      """ Return a new instance of the genome
      
      :rtype: the new GTreeGP instance
      """
      newcopy = GTreeGP()
      self.copy(newcopy)
      newcopy.processNodes(True)
      return newcopy

   def compare(self, other):
      """ This method will compare the currently tree with another one

      :param other: the other GTreeGP to compare
      """
      if not isinstance(other, GTreeGP):
         Util.raiseException("The other tree used to compare is not a GTreeGP class", TypeError)

      stack_self = []
      stack_other = []

      tmp_self  = None
      tmp_other = None

      stack_self.append(self.getRoot())
      stack_other.append(other.getRoot())

      while len(stack_self) > 0:

         if (len(stack_self) <= 0) or (len(stack_other) <= 0):
            return -1
         
         tmp_self  = stack_self.pop()
         tmp_other = stack_other.pop()

         if tmp_self.compare(tmp_other) <> 0:
            return -1

         rev_childs = tmp_self.getChilds()
         stack_self.extend(rev_childs)

         rev_childs = tmp_other.getChilds()
         stack_other.extend(rev_childs)
   
      return 0


#################################
#    Tree GP Utility Functions  # 
#################################

def buildGTreeGPGrow(ga_engine, depth, max_depth):
   """ Creates a new random GTreeGP root node with subtrees using
   the "Grow" method.
   
   :param ga_engine: the GA Core
   :param depth: the initial depth
   :max_depth: the maximum depth of the tree
   :rtype: the root node
   """

   gp_terminals = ga_engine.getParam("gp_terminals")
   assert gp_terminals is not None

   gp_function_set = ga_engine.getParam("gp_function_set")
   assert gp_function_set is not None

   if depth == max_depth:
      random_terminal = rand_choice(gp_terminals)
      n = GTreeNodeGP(random_terminal, Consts.nodeType["TERMINAL"])
      return n
   else:
      # Do not generate degenerative trees 
      if depth == 0:
         random_node = rand_choice(gp_function_set.keys())
      else:
         fchoice = rand_choice([gp_function_set.keys(), gp_terminals])
         random_node = rand_choice(fchoice)

      if random_node in gp_terminals:
         n = GTreeNodeGP(random_node, Consts.nodeType["TERMINAL"])
      else:
         n = GTreeNodeGP(random_node, Consts.nodeType["NONTERMINAL"])

   if n.getType() == Consts.nodeType["NONTERMINAL"]:
      for i in xrange(gp_function_set[n.getData()]):
         child = buildGTreeGPGrow(ga_engine, depth+1, max_depth)
         child.setParent(n)
         n.addChild(child)

   return n

def buildGTreeGPFull(ga_engine, depth, max_depth):
   """ Creates a new random GTreeGP root node with subtrees using
   the "Full" method.
   
   :param ga_engine: the GA Core
   :param depth: the initial depth
   :max_depth: the maximum depth of the tree
   :rtype: the root node
   """
   gp_terminals = ga_engine.getParam("gp_terminals")
   assert gp_terminals is not None

   gp_function_set = ga_engine.getParam("gp_function_set")
   assert gp_function_set is not None

   if depth == max_depth:
      random_terminal = rand_choice(gp_terminals)
      n = GTreeNodeGP(random_terminal, Consts.nodeType["TERMINAL"])
      return n
   else:
      random_oper = rand_choice(gp_function_set.keys())
      n = GTreeNodeGP(random_oper, Consts.nodeType["NONTERMINAL"])

   if n.getType() == Consts.nodeType["NONTERMINAL"]:
      for i in xrange(gp_function_set[n.getData()]):
         child = buildGTreeGPFull(ga_engine, depth+1, max_depth)
         child.setParent(n)
         n.addChild(child)

   return n
