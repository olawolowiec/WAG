import unittest   # The test framework

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

class Test_Logic(unittest.TestCase):
    def test_if(self):
        self.assertEqual(1, wag.WagOperation(
        """  
        ZMIENNA a=1
        JEŻELI a==2 WYKONAJ false BĄDŹ a==3 WYKONAJ false PRZECIWNIE true
        """
        ,1))

    def test_if_multiline(self):
        self.assertEqual(1, wag.WagOperation(
        """  
        ZMIENNA a=2;
        JEŻELI a==1 WYKONAJ; PRINT(1); PRINT(2); BĄDŹ a==2 WYKONAJ; PRINT(3); PRINT(4); PRZECIWNIE PRINT(5); PODSUMOWUJĄC
        """
        ,1))

class Test_Loop(unittest.TestCase):
    def test_for(self):
        self.assertEqual(45, wag.WagOperation(
        """  
        ZMIENNA a = 0
        DLA i=0 DO 10 WYKONAJ;
        ZMIENNA a=a+i; 
        CO_KOŃCZY_DOWÓD
        a
        """
        ,2))

    def test_while(self):
         self.assertEqual(5, wag.WagOperation(
        """  
        ZMIENNA a = 0;
        DOPÓKI a < 5 DOPÓTY ZMIENNA a= a+1;
        a;
        """
        ,2))

if __name__ == '__main__':
    unittest.main()