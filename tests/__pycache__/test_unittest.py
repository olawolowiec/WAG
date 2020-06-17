import unittest   # The test framework
#from wag import *
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import wag

class Test_TestArytmetic(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(15, wag.WagOperation('10 + 5'))
  
    def test_submission(self):
        self.assertEqual(5, wag.WagOperation('10 - 5'))

    def test_division(self):
        self.assertEqual(5, wag.WagOperation('10 / 2'))

    def test_multiply(self):
        self.assertEqual(50, wag.WagOperation('10 * 5'))

    def test_power(self):
        self.assertEqual(50, wag.WagOperation('10 * 5'))

    def test_advance_arytmetic(self):
        self.assertEqual(6, wag.WagOperation('2 + (2 * 2)'))

class Test_TestFunction(unittest.TestCase):
    def test_function_without_parameters(self):
        self.assertEqual(5, wag.WagOperation(
        """  TEZA test();
             ZMIENNA foo=5;
             PODSUMOWUJĄC foo;
             CO_KOŃCZY_DOWÓD;
             
             test()
        """
        ,1))

    def test_function_with_parameters(self):
        self.assertEqual(5, wag.WagOperation(
        """  TEZA test(a,b);
             ZMIENNA foo= a+b;
             PODSUMOWUJĄC foo;
             CO_KOŃCZY_DOWÓD;
             
             test(2,3)
        """
        ,1))





if __name__ == '__main__':
    unittest.main()