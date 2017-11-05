import unittest
from unittest import TestLoader, TextTestRunner, TestSuite
from Functions import formatDate
from Sprint1 import birthBeforeMarriage_us02
from Sprint1 import birthBeforeDeath_us03
from Sprint1 import birth_Before_Death_of_Parents_US09,fewer_than_fifteen_siblings_US15
from Sprint1 import individualAge_us27, checkBigamy_us11
from Sprint2 import divorceBeforCurrentDate_us01,birthdayBeforeCurrentDate_us01,marriageBeforCurrentDate_us01,deathBeforCurrentDate_us01, lessThan150Years_US07
from Sprint2 import marriedToDescendants_us17, marriedToSiblings_us18
from Sprint2 import correct_gender_for_role_US21,list_of_deceased_US29
from Sprint2 import recent_deaths_us36, living_single_us31
from Sprint3 import siblingSpacing_us13, firstCousinsMarried_us19
from Sprint3 import List_living_married_US30,List_recent_births_US35
from Sprint3 import checkMarriageBeforeDivorce_us04, checkMarriageBeforeDeath_us05
from Sprint3 import List_large_age_difference_US34, Recent_surviors_US37
from Sprint4 import correspondingEntries_us26, orderSiblings_us28
import logging

class TestFamily(unittest.TestCase):
     
    def setUp(self):
        from Individual import Individual
        self=Individual(0)

    def test_List_large_age_difference_US34(self):
        from Individual import Individual
        from Family import Family
        list1 = {'A1': Individual('A1', age='106'),
                 'A2': Individual('A1', age='39')}

        list2 = {'B1': Family('B1', husband = 'A1', wife = 'A2')}
        
        self.assertFalse(List_large_age_difference_US34( list1, list2))
        

    def test_Recent_surviors_US37(self):
        from Individual import Individual
        from Family import Family
        list1 = {'A1': Individual('A1', death='2017-10-29'),
                 'A2': Individual('A1', birthday='1960-03-12'),
                 'A3': Individual('A1', birthday='1993-03-12')}
        list2 = {'B1': Family('B1', husband = 'A1', wife = 'A2')}
        children = ['A3']
        for child in children:
            list2['B1'].setChildren(child)
        self.assertFalse(Recent_surviors_US37( list1, list2))
        

 
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


    def test_recent_death_us36(self):
        from Individual import Individual
        self.assertEqual (recent_deaths_us36(Individual(self,10, death = '2017-10-10')),False)
        self.assertFalse(recent_deaths_us36(Individual(self,10,death ='1845-10-05')))
        self.assertFalse(recent_deaths_us36(Individual(self,10,death ='2017-10-10')))

    def test_living_single_us31(self):
        from Individual import Individual
        self.assertEqual (living_single_us31(Individual(self, 10, birthday = '1977-12-17')), False)
        

    def test_lessThan150Years_US07(self):
        #from Individual import birthBeforeMarriage
        from Individual import Individual
        self.assertEqual( lessThan150Years_US07(Individual(self, 10,birthday = '1945-01-05')), True)
        self.assertFalse(lessThan150Years_US07(Individual(self,10,birthday ='1845-10-05')))
        self.assertFalse(lessThan150Years_US07(Individual(self,10,birthday ='1845-10-05',death='2010-10-05')))
    

    def test_individualAge_us27(self):
        from Individual import Individual
        self.assertEqual(individualAge_us27(Individual(self, 10, birthday = '1977-10-14')), 40)
        self.assertEqual(individualAge_us27(Individual(self, 10, birthday = '1977-01-29')), 40)
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

    def test_fewer_than_fifteen_siblings_US15(self):
        from Individual import Individual
        from Family import Family
        ls1 = {'A1': Individual('A1', 'NA', 'M', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A2': Individual('A2', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A3': Individual('A3', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A4': Individual('A4', 'NA', 'M', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A5': Individual('A5', 'NA', 'M', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A6': Individual('A6', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A7': Individual('A7', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A8': Individual('A8', 'NA', 'M', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A9': Individual('A9', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A10': Individual('A10', 'NA', 'M', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A11': Individual('A11', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A12': Individual('A12', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A13': Individual('A13', 'NA', 'M', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A14': Individual('A14', 'NA', 'M', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A15': Individual('A15', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A16': Individual('A16', 'NA', 'M', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A17': Individual('A17', 'NA', 'M', 'NA', 'NA', 'NA', 'NA', 'F1')}
        ls2 = {'F1': Family('F1', husband = 'A1', wife = 'A2', marriage = '1990-03016', divorce = 'NA')}
        children =['A3','A4','A5','A6','A7','A8','A9','A10','A11','A12','A13','A14','A15','A16','A17']
        for child in children:
            ls2['F1'].setChildren(child)
        self.assertFalse(fewer_than_fifteen_siblings_US15(ls2))

    def test_correct_gender_for_role_US21(self):
        from Individual import Individual
        from Family import Family
        ls1 = {'A1': Individual('A1', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A2': Individual('A2', 'NA', 'M', 'NA', 'NA', 'NA', 'NA', 'F1'),}
        ls2 = {'F1': Family('F1', husband = 'A1', wife = 'A2', marriage = formatDate('16 MAR 1990'), divorce = 'NA')}
        self.assertFalse(correct_gender_for_role_US21(ls1['A1'],ls2))

    def test_list_of_deceased_US29(self):
        from Individual import Individual
        self.assertFalse(list_of_deceased_US29(Individual(self,10,death= '1950-08-14')))


    def test_siblingSpacing_us13(self):
        from Individual import Individual
        from Family import Family
        list1 = {'B1': Family('B1')}
        children = ['A3', 'A4', 'A5']
        for child in children:
            list1['B1'].setChildren(child)
        #Spacing violated by less than 8 months condition
        list2 = {'A3': Individual('A1', birthday = '1980-01-01'),
                 'A4': Individual('A2', birthday = '1987-02-05'),
                 'A5': Individual('A3', birthday = '1980-07-01')}        
        self.assertTrue(siblingSpacing_us13(list1['B1'],list2))
        #Spacing violated by more than 2 days condition
        list3 = {'A3': Individual('A1', birthday = '1980-01-01'),
                 'A4': Individual('A2', birthday = '1987-02-05'),
                 'A5': Individual('A3', birthday = '1980-01-03')}        
        self.assertTrue(siblingSpacing_us13(list1['B1'],list2))
        #Spacing not violated
        list4 = {'A3': Individual('A1', birthday = '1980-01-01'),
                 'A4': Individual('A2', birthday = '1987-02-05'),
                 'A5': Individual('A3', birthday = '1984-01-03')}        
        self.assertFalse(siblingSpacing_us13(list1['B1'],list4))


    def test_firstCousinsMarried_us19(self):
        from Individual import Individual
        from Family import Family    
        list1 = {'A1': Individual('A1', childFamily = 'B1'),
                 'A2': Individual('A1'),
                 'A3': Individual('A3', childFamily = 'B1', spouseFamily = 'B3'),
                 'A4': Individual('A4', childFamily = 'B2', spouseFamily = 'B4')}
        #Married to first cousin
        list2 = {'B1': Family('B1'),
                 'B2': Family('B2', husband = 'A1', wife = 'A2'),
                 'B3': Family('B3', husband = 'A3'),
                 'B4': Family('B4', husband = 'A4', wife = 'A5')}
        children = ['A1', 'A3']
        for child in children:
            list2['B1'].setChildren(child)
        list2['B2'].setChildren('A4')
        cousins = ['A5', 'A6']
        for cousin in cousins:
            list2['B3'].setChildren(cousin)        
        self.assertTrue(firstCousinsMarried_us19(list1['A4'], list1, list2))
        #Not married to first cousin
        list3 = {'B1': Family('B1'),
                 'B2': Family('B2', husband = 'A1', wife = 'A2'),
                 'B3': Family('B3'),
                 'B4': Family('B4', husband = 'A4', wife = 'A7')}
        self.assertFalse(firstCousinsMarried_us19(list1['A4'], list1, list3))

    def test_List_living_married_US30(self):
        from Individual import Individual
        from Family import Family
        ls1 = {'A1': Individual('A1', 'NA', 'F', 'NA', 'NA', 'NA', 'NA', 'F1'),
                 'A2': Individual('A2', 'NA', 'M', 'NA', 'NA', 'NA', 'NA', 'F1'),}
        ls2 = {'F1': Family('F1', husband = 'A1', wife = 'A2', marriage = formatDate('16 MAR 1990'), divorce = 'NA')}
        self.assertFalse(List_living_married_US30(ls1['A1'],ls2))

    def test_List_recent_births_US35(self):
        from Individual import Individual
        self.assertFalse(List_recent_births_US35(Individual(self,10,death= '2017-09-1')))

    def test_checkMarriageBeforeDivorce_us04(self):
        from Family import Family
        self.assertEqual( checkMarriageBeforeDivorce_us04(Family(self, 10,marriage = '1915-10-05')), True)
        self.assertTrue(checkMarriageBeforeDivorce_us04(Family(self,10,marriage ='1945-10-05',divorce= '1975-03-10')))
        self.assertTrue(checkMarriageBeforeDivorce_us04(Family(self,10,marriage ='1945-10-05',divorce= '1945-11-10')))
        self.assertTrue(checkMarriageBeforeDivorce_us04(Family(self,10,marriage ='1945-11-05',divorce= '1945-11-10')))
        self.assertFalse(checkMarriageBeforeDivorce_us04(Family(self,10,marriage ='1945-01-05',divorce= '1935-03-10')))
        self.assertFalse(checkMarriageBeforeDivorce_us04(Family(self,10,divorce= '1935-03-10')))
        self.assertFalse(checkMarriageBeforeDivorce_us04(Family(self,10)))

    def test_checkMarriageBeforeDeath_us05(self):
        from Family import Family
        from Individual import Individual
        self.assertEqual( checkMarriageBeforeDeath_us05(Family(self, 10,marriage = '1945-10-05'),Individual(self,10,birthday='1915-10-05')), True)
        self.assertTrue(checkMarriageBeforeDeath_us05(Family(self,10,marriage ='1945-10-05'),Individual(self,10,birthday='1915-10-05',death= '1975-03-10')))
        self.assertTrue(checkMarriageBeforeDeath_us05(Family(self,10,marriage ='1945-10-05'),Individual(self,10,birthday='1915-10-05',death= '1945-11-10')))
        self.assertTrue(checkMarriageBeforeDeath_us05(Family(self,10,marriage ='1945-10-05'),Individual(self,10,birthday='1915-10-05',death= '1945-11-10')))
        self.assertFalse(checkMarriageBeforeDeath_us05(Family(self,10,marriage ='1945-10-05'),Individual(self,10,birthday='1915-10-05',death= '1935-03-10')))
        self.assertFalse(checkMarriageBeforeDeath_us05(Family(self,10,),Individual(self,10,birthday='1915-10-05')))
        self.assertFalse(checkMarriageBeforeDeath_us05(Family(self,10,marriage ='1945-10-05'),Individual(self,10)))

    def test_correspondingEntries_us26(self):
        from Family import Family
        from Individual import Individual
        list1 = {'A1': Individual('A1', spouseFamily = 'B2'), #husband
                 'A2': Individual('A2', spouseFamily = 'B2'), #wife
                 'A5': Individual('A5', childFamily = 'B2')}  #child 
        #Family's husband does not have the same listed as his spouse Family:
        list2 = {'B1': Family('B1', husband = 'A1', wife = 'A5')}
        self.assertTrue(correspondingEntries_us26(list2['B1'],list1))
        #Family's wife does not have the same listed as her spouse Family:
        list2 = {'B1': Family('B1', husband = 'A5', wife = 'A1')}
        self.assertTrue(correspondingEntries_us26(list2['B1'],list1))
        #Family's child does not have the same listed as his/her child Family:
        list2 = {'B2': Family('B1', husband = 'A1', wife = 'A2')}
        list2['B2'].setChildren('A5')
        self.assertTrue(correspondingEntries_us26(list2['B2'],list1))
        #All the roles match in individual and family tables:
        list1 = {'A1': Individual('A1', spouseFamily = 'B1'),
                 'A2': Individual('A2', spouseFamily = 'B1'),
                 'A5': Individual('A5', childFamily = 'B1')}
        self.assertFalse(correspondingEntries_us26(list2['B2'],list1))

    def test_orderSiblings_us28(self):
        from Family import Family
        from Individual import Individual
        list1 = {'A1': Individual('A1', childFamily = 'B1', age = '48'),
                 'A2': Individual('A2', childFamily = 'B1', age = '31'),
                 'A3': Individual('A3', childFamily = 'B1', age = '37')}
        list2 = {'B1': Family('B1')}
        children = ['A1', 'A2', 'A3']
        for child in children:
            list2['B1'].setChildren(child)
        self.assertEqual(orderSiblings_us28(list2['B1'], list1), 'B1 A1 A3 A2')

if __name__ == '__main__':
    #logging.basicConfig( stream=sys.stderr )
    #logging.getLogger( "TestFamily.test_birth_Before_Death" ).setLevel( logging.DEBUG )
    #logging.getLogger( "TestFamily.test_birth_Before_Marriage" ).setLevel( logging.DEBUG )
    unittest.main()
