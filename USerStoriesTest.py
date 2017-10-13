import unittest
from unittest import TestLoader, TextTestRunner, TestSuite
from Sprint1 import birthBeforeMarriage_us02
from Sprint1 import birthBeforeDeath_us03
from Sprint2 import divorceBeforCurrentDate_us01,birthdayBeforeCurrentDate_us01,marriageBeforCurrentDate_us01,deathBeforCurrentDate_us01, lessThan150Years_US07
import logging



class TestFamily(unittest.TestCase):
     
    def setUp(self):
        from Individual import Individual
        self=Individual(0)
 
    def test_birth_Before_Marriage_us02(self):
        #from Individual import birthBeforeMarriage
        from Individual import Individual
        self.assertEqual( birthBeforeMarriage_us02(Individual(self, 10,birthday = '5 JAN 1945')), True)
        self.assertTrue(birthBeforeMarriage_us02(Individual(self,10,birthday ='1945-10-05',marriage= '1975-03-10')))
        self.assertTrue(birthBeforeMarriage_us02(Individual(self,10,birthday ='1945-10-05',marriage= '1945-11-10')))
        self.assertTrue(birthBeforeMarriage_us02(Individual(self,10,birthday ='1945-11-05',marriage= '1945-11-10')))
        self.assertFalse(birthBeforeMarriage_us02(Individual(self,10,birthday ='1945-01-05',marriage= '1935-03-10')))
        self.assertFalse(birthBeforeMarriage_us02(Individual(self,10,marriage= '1935-03-10')))
        self.assertFalse(birthBeforeMarriage_us02(Individual(self,10)))


    def test_birth_Before_Death_us03(self):
        #from Individual import birthBeforeMarriage
        from Individual import Individual
        self.assertEqual( birthBeforeDeath_us03(Individual(self, 10,birthday = '5 JAN 1945')), True)
        self.assertTrue(birthBeforeDeath_us03(Individual(self,10,birthday ='1945-10-05',death= '1975-03-10')))
        self.assertTrue(birthBeforeDeath_us03(Individual(self,10,birthday ='1945-10-05',death= '1945-11-10')))
        self.assertTrue(birthBeforeDeath_us03(Individual(self,10,birthday ='1945-11-05',death= '1945-11-10')))
        self.assertFalse(birthBeforeDeath_us03(Individual(self,10,birthday ='1945-01-05',death= '1935-03-10')))
        self.assertFalse(birthBeforeDeath_us03(Individual(self,10,death= '1935-03-10')))
        self.assertFalse(birthBeforeDeath_us03(Individual(self,10)))
        

    def test_datesBeforeCurrentDate_US01(self):
        #from Individual import birthBeforeMarriage
        from Individual import Individual
        self.assertEqual( divorceBeforCurrentDate_us01('1945-01-05'), True)
        self.assertFalse(divorceBeforCurrentDate_us01('2045-03-10'))
        self.assertFalse(birthdayBeforeCurrentDate_us01('2045-03-10'))
        self.assertFalse(birthdayBeforeCurrentDate_us01('NA'))
        self.assertTrue(birthdayBeforeCurrentDate_us01('2015-03-10'))
        self.assertTrue(marriageBeforCurrentDate_us01('2015-03-10'))
        self.assertTrue(deathBeforCurrentDate_us01('2015-03-10'))
        

    def test_lessThan150Years_US07(self):
        #from Individual import birthBeforeMarriage
        from Individual import Individual
        self.assertEqual( lessThan150Years_US07(Individual(self, 10,birthday = '1945-01-05')), True)
        self.assertFalse(lessThan150Years_US07(Individual(self,10,birthday ='1845-10-05')))
        self.assertFalse(lessThan150Years_US07(Individual(self,10,birthday ='1845-10-05',death='2010-10-05')))
        
 
if __name__ == '__main__':
    #logging.basicConfig( stream=sys.stderr )
    #logging.getLogger( "TestFamily.test_birth_Before_Death" ).setLevel( logging.DEBUG )
    #logging.getLogger( "TestFamily.test_birth_Before_Marriage" ).setLevel( logging.DEBUG )
    unittest.main()