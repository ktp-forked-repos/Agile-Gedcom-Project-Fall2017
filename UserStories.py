import datetime
from Parser import individualTable, familyTable
from Functions import checkDate

def userStories(individualList, familyList):
 
    # Sprint 1 stories:
    individualAge(individualList)
    checkBigamy(individualList, familyList)

########################################################################################################################################################################
def individualAge(individualList):
    """ US27 : Include individual ages """ 
    ages = []     
    for indi in individualList:
        birth = individualList[indi].getBirthday().split("-")

        birthyear = int(birth[0])
        birthmonth = int(birth[1])
        birthdate = int(birth[2])

        today = datetime.date.today()

        age = today.year - birthyear
        if (today.month < birthmonth):
            age -= 1;
        elif (today.month == birthmonth):
            if (today.day < birthdate):
                age -= 1;

        ages.append(age)
        individualList[indi].setAge(age)
        """name = individualList[indi].name.split("/")
        firstName = name[0]
        lastName = name[1]
        print  firstName + lastName + ": " + str(age) + " years" """

    # Each individual's current age when listing
    #outputFile = open('Parser_Output.txt', 'w')
    #individualTable.add_column(["Age",ages])

#########################################################################################################################################################################
def checkBigamy(individualList, familyList):
    """ US11 : No bigamy """
    for indi in individualList:
        if (individualList[indi].spouseFamily != 'NA'):   # Exclude the un-married people
            for fam in familyList:
                # Enter only if the person is a spouse in any other family apart from the one he/ she is currently a spouse in.     
                if (fam != individualList[indi].spouseFamily and (individualList[indi].ID == familyList[fam].husband or individualList[indi].ID == familyList[fam].wife)):

                    firstMarriage = familyList[individualList[indi].spouseFamily]
                    secondMarriage = familyList[fam]
                    # Check for the first and second marriages depending on the marriage dates
                    if (checkDate(firstMarriage.marriage, secondMarriage.marriage) == False):
                        temp = firstMarriage
                        firstMarriage = secondMarriage
                        secondMarriage = temp

                    # Check if the person got married 2nd time even when he/ she has not yet been divorced from the 1st marriage
                    if (firstMarriage.divorce == 'NA'):
                        # Then check if the spouse from the 1st marriage is still alive for bigamy to take place
                        if (individualList[indi].ID == firstMarriage.husband):
                            if (isAlive(individualList[firstMarriage.wife])):
                                pass
                                #bigamy = True       
                                #print an error message on the screen/ call a function
                        elif (individualList[indi].ID == firstMarriage.wife):
                            if (isAlive(individualList[firstMarriage.husband])):
                                pass
                                #bigamy = True    
                                #print an error message on the screen/ call a function
                        
                    # Otherwise check if the person was once invloved in bigamy
                    else:
                        # If the person got divorced from 1st marriage after marrying the 2nd time
                        if (checkDate(secondMarriage.marriage, firstMarriage.divorce)):
                            pass
                            #bigamy = True
                            #print an error message on the screen/ call a function

###########################################################################################################################################################################
def isAlive(person):
    """ Function to check if a person is still alive 
        ** Not a user story """
    if (person.death != 'NA'):
        return False
    else:
        return True

########################################################################################################################################################################
def US09_birthBeforeDeath(individualList, familyList)
    father_death=23
    mother_death=34
    child_birth=23
