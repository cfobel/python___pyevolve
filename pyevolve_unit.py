import unittest
import types

from pyevolve import FunctionSlot

def func_test(val):
   return val

def func_test2(val):
   return val

class TestFunctionSlot(unittest.TestCase):

   def setUp(self):
      self.slot = FunctionSlot.FunctionSlot("Test Slot")
     
   def test_add(self):
      self.slot.clear()
      self.slot += func_test
      self.assertEqual(len(self.slot), 1)
      f1 = self.slot[0]
      self.assertEqual(f1, func_test)
      self.slot[0] = func_test2
      self.assertEqual(len(self.slot), 1)
      self.assertEqual(self.slot[0], func_test2)
      self.slot.clear()
      self.assertEqual(len(self.slot), 0)
      self.assertTrue(self.slot.isEmpty())
      self.slot.set(func_test)
      self.assertEqual(len(self.slot), 1)

   def test_apply(self):
      self.slot.clear()
      self.slot += func_test
      self.assertEqual(self.slot.apply(0, 1), 1)

      s = 0
      for it in self.slot.applyFunctions(1):
         s += it
      self.assertEqual(s, 1)

      self.slot += func_test2
      s = 0
      for it in self.slot.applyFunctions(1):
         s += it
      self.assertEqual(s, 2)

   def test_typecheck(self):
      self.assertRaises(TypeError, self.slot.setRandomApply, "")
      self.assertRaises(TypeError, self.slot.__iadd__, "")
      self.assertRaises(TypeError, self.slot.__setitem__, "")
      self.assertRaises(TypeError, self.slot.add, "")
      self.assertRaises(TypeError, self.slot.set, "")
 
   def test_others(self):
      self.slot.clear()
      self.slot += func_test2
      for it in self.slot:
         self.assertEqual(it, func_test2)

if __name__ == '__main__':
   suite = unittest.TestLoader().loadTestsFromTestCase(TestFunctionSlot)
   unittest.TextTestRunner(verbosity=2).run(suite)
