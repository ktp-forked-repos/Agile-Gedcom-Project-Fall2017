import unittest
from unittest import TestLoader, TextTestRunner, TestSuite
from UserStories import birthBeforeMarriage_us02
from UserStories import birthBeforeDeath_us03
import logging



class TestFamily(unittest.TestCase):
     
    def setUp(self):
        from Individual import Individual
        self=Individual(0)
 
    def test_birth_Before_Marriage(self):
        #from Individual import birthBeforeMarriage
        from Individual import Individual
        self.assertEqual( birthBeforeMarriage_us02(Individual(self, 10,birthday = '5 JAN 1945')), True)
        self.assertTrue(birthBeforeMarriage_us02(Individual(self,10,birthday ='1945-10-05',marriage= '1975-03-10')))
        self.assertTrue(birthBeforeMarriage_us02(Individual(self,10,birthday ='1945-10-05',marriage= '1945-11-10')))
        self.assertTrue(birthBeforeMarriage_us02(Individual(self,10,birthday ='1945-11-05',marriage= '1945-11-10')))
        self.assertFalse(birthBeforeMarriage_us02(Individual(self,10,birthday ='5 Jan 1945',marriage= '10 March 1935')))
        self.assertFalse(birthBeforeMarriage_us02(Individual(self,10,marriage= '10 March 1935')))
        self.assertFalse(birthBeforeMarriage_us02(Individual(self,10)))


    def test_birth_Before_Death(self):
        #from Individual import birthBeforeMarriage
        from Individual import Individual
        self.assertEqual( birthBeforeDeath_us03(Individual(self, 10,birthday = '5 JAN 1945')), True)
        self.assertTrue(birthBeforeDeath_us03(Individual(self,10,birthday ='1945-10-05',death= '1975-03-10')))
        self.assertTrue(birthBeforeDeath_us03(Individual(self,10,birthday ='1945-10-05',death= '1945-11-10')))
        self.assertTrue(birthBeforeDeath_us03(Individual(self,10,birthday ='1945-11-05',death= '1945-11-10')))
        self.assertFalse(birthBeforeDeath_us03(Individual(self,10,birthday ='5 Jan 1945',death= '10 March 1935')))
        self.assertFalse(birthBeforeDeath_us03(Individual(self,10,death= '10 March 1935')))
        self.assertFalse(birthBeforeDeath_us03(Individual(self,10)))
 
if __name__ == '__main__':
    #logging.basicConfig( stream=sys.stderr )
    #logging.getLogger( "TestFamily.test_birth_Before_Death" ).setLevel( logging.DEBUG )
    #logging.getLogger( "TestFamily.test_birth_Before_Marriage" ).setLevel( logging.DEBUG )
    unittest.main()