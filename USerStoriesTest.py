import unittest
from unittest import TestLoader, TextTestRunner, TestSuite
from Functions import formatDate
from Sprint1 import birthBeforeMarriage_us02
from Sprint1 import birthBeforeDeath_us03
from Sprint1 import individualAge_us27, checkBigamy_us11
from Sprint2 import divorceBeforCurrentDate_us01,birthdayBeforeCurrentDate_us01,marriageBeforCurrentDate_us01,deathBeforCurrentDate_us01, lessThan150Years_US07
from Sprint2 import marriedToDescendants_us17, marriedToSiblings_us18
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
    

    def test_individualAge_us27(self):
        from Individual import Individual
        self.assertEqual(individualAge_us27(Individual(self, 10, birthday = '1977-10-14')), 40)
        self.assertEqual(individualAge_us27(Individual(self, 10, birthday = '1977-10-29')), 39)
        self.assertEqual(individualAge_us27(Individual(self, 10, birthday = '1977-09-14')), 40)
        self.assertEqual(individualAge_us27(Individual(self, 10, birthday = '1977-12-17')), 39)


    def test_checkBigamy_us11(self):
        from Individual import Individual
        from Family import Family
        #No bigamy
        list1 = {'A1': Individual('A1', 'NA', 'M', 'NA', 'NA', 'NA', 'NA', 'B1'),
                 'A2': Individual('A2', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'B1'),
                 'A3': Individual('A3', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'B2')}
        list2 = {'B1': Family('B1', husband = 'A1', wife = 'A2', marriage = formatDate('31 JAN 1969'), divorce = formatDate('16 NOV 1980')),
                 'B2': Family('B2', husband = 'A1', wife = 'A3', marriage = formatDate('1 JAN 1982'), divorce = 'NA')}
        self.assertFalse(checkBigamy_us11(list1['A1'], list1, list2))
        #Bigamy
        list3 = {'A1': Individual('A1', 'NA', 'M', 'NA', 'NA', 'NA', 'NA', 'B1'),
                 'A2': Individual('A2', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'B1'),
                 'A3': Individual('A3', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'B2')}
        list4 = {'B1': Family('B1', husband = 'A1', wife = 'A2', marriage = formatDate('31 JAN 1969'), divorce = formatDate('16 NOV 1980')),
                 'B2': Family('B2', husband = 'A1', wife = 'A3', marriage = formatDate('6 AUG 1979'), divorce = 'NA')}
        self.assertTrue(checkBigamy_us11(list3['A1'], list3, list4))      


    def test_marriedToDescendants_us17(self):
        from Individual import Individual
        from Family import Family
        list1 = {'A1': Individual('A1', spouseFamily = 'B1'),
                 'A3': Individual('A1', spouseFamily = 'NA'),
                 'A4': Individual('A1', spouseFamily = 'NA'),
                 'A5': Individual('A1', spouseFamily = 'B2'),
                 'A7': Individual('A1', spouseFamily = 'NA'),
                 'A8': Individual('A1', spouseFamily = 'B3')}

        #Parent married to child
        list2 = {'B1': Family('B1', husband = 'A1', wife = 'A2'),
                  'B2': Family('B2', husband = 'A1', wife = 'A5')}
        children = ['A3', 'A4', 'A5']
        for child in children:
            list2['B1'].setChildren(child)
        self.assertTrue(marriedToDescendants_us17(list1['A1'], list1, list2))

        #Parent married to grand child
        list3 = {'B1': Family('B1', husband = 'A1', wife = 'A2'),
                 'B2': Family('B2', husband = 'A3', wife = 'A6'),
                 'B3': Family('B3', husband = 'A1', wife = 'A8')}
        children = ['A3', 'A4', 'A5']
        for child in children:
            list3['B1'].setChildren(child)
        grandChildren = ['A7', 'A8']
        for grandChild in grandChildren:
            list3['B2'].setChildren(grandChild)                
        self.assertTrue(marriedToDescendants_us17(list1['A1'], list1, list3))


    def test_marriedToSiblings_us18(self):  
        from Individual import Individual
        from Family import Family
        #Married to sibling
        list1 = {'A3': Individual('A3', childFamily = 'B1', spouseFamily = 'B2')}
        list2 = {'B1': Family('B1', husband = 'A1', wife = 'A2'),
                 'B2': Family('B2', husband = 'A3', wife = 'A5')}
        children = ['A3', 'A4', 'A5']
        for child in children:
            list2['B1'].setChildren(child)
        self.assertTrue(marriedToSiblings_us18(list1['A3'], list2))
        #Not married to sibling
        list3 = {'B1': Family('B1', husband = 'A1', wife = 'A2'),
                 'B2': Family('B2', husband = 'A3', wife = 'A6')}
        children = ['A3', 'A4', 'A5']
        for child in children:
            list3['B1'].setChildren(child)
        self.assertFalse(marriedToSiblings_us18(list1['A3'], list3))

 
if __name__ == '__main__':
    #logging.basicConfig( stream=sys.stderr )
    #logging.getLogger( "TestFamily.test_birth_Before_Death" ).setLevel( logging.DEBUG )
    #logging.getLogger( "TestFamily.test_birth_Before_Marriage" ).setLevel( logging.DEBUG )
    unittest.main()