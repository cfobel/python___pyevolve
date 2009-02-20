import inspect

NODE_CONSTANT = 0
NODE_VARIABLE = 1
NODE_OPERATOR = 2

NODE_TYPE = ["Constant", "Variable", "Operator"]

class GTreeNodeBase:
   def __init__(self, parent):
      self.parent = parent
      self.childs = []

   def getChilds(self):
      return self.childs
   
   def addChild(self, child):
      if not isinstance(child, GTreeNodeBase):
         print "error: the child parameter is not a GTreeNodeBase"
      self.childs.append(child)

   def setParent(self, parent):
      self.parent = parent
   
   def getParent(self):
      return self.parent

   def __len__(self):
      return len(self.childs)


class GTreeNodeGP(GTreeNodeBase):
   def __init__(self, data, node_type=NODE_OPERATOR, parent=None):
      GTreeNodeBase.__init__(self, parent)
      self.node_type = node_type
      self.node_data = data

   def newNode(self, data, node_type=NODE_OPERATOR):
      node = GTreeNodeGP(data, node_type, self)
      self.addChild(node)
      return node

   def __repr__(self):
      str_repr = "GTreeNode [%s @ %s]" % (NODE_TYPE[self.node_type], self.node_data)
      return str_repr


class GTreeBase:
   def __init__(self, root_node):
      self.root_node = root_node

   def getRoot(self):
      return self.root_node
   
   def setRoot(self, root):
      self.root_node = root

   def getNodesCount(self, start_node=None):
      count = 1
      if start_node is None:
         start_node = self.getRoot()
      for i in start_node.getChilds():
         count += self.getNodesCount(i)
      return count
   
   def getTraversalString(self, start_node=None, spc=0):
      str_buff = ""
      if start_node is None:
         start_node = self.getRoot()
         str_buff += "%s\n" % start_node
      x = spc + 2
      for i in start_node.getChilds():
         str_buff += "%s%s\n" % (" " * x, i)
         str_buff += self.getTraversalString(i, x)
      return str_buff

   def traversal(self, callback, start_node=None):
      if not inspect.isfunction(callback):
         print "error: not function callback"

      if start_node is None:
         start_node = self.getRoot()
         callback(start_node)
      for i in start_node.getChilds():
         callback(i)
         self.traversal(callback, i)

   def __repr__(self):
      return "- GTree\n" + self.getTraversalString()

   def __len__(self):
      return self.getNodesCount()
   
class GTreeGP(GTreeBase):
   
   def __init__(self, root_node=None):
      GTreeBase.__init__(self, root_node)


def show(node):
   print node

if __name__ == "__main__":
   root = GTreeNodeGP("root")
   t = GTreeGP(root)
   n2 = root.newNode("teste2")
   n3 = root.newNode("teste3")
   n4 = n3.newNode("teste4")
   n5 = n3.newNode("teste5")
   n6 = n5.newNode("teste6")
   n7 = root.newNode("teste7")


   print t
   print "Len:", len(t)
   t.traversal(show)




