import datetime
from Parser import individualTable, familyTable
from Functions import checkDate

def userStories(individualList, familyList):
<<<<<<< HEAD
=======

    outputFile = open('Parser_Output.txt', 'a')
    outputFile.write('\n' + "{0:^150}".format(" Error Report ") + '\n' + '\n')
    outputFile.write('\t' + 'Tag' + '\t' + '\t' + 'Concerned' + '\t' + '\t' + 'User Story' + '\t' + '\t' + '\t' + 'Description' + '\t' + '\t' + '\t' + '\t' + '\t' +  '\t' + 'Location' + '\n' +'\n')
    outputFile.close()
>>>>>>> 8bf1f2cf236fab60219dfa6bc1d20368a7e6adf8
 
    # Sprint 1 stories:
    individualAge(individualList)
    checkBigamy(individualList, familyList)

########################################################################################################################################################################
def individualAge(individualList):
    """ US27 : Include individual ages """ 
<<<<<<< HEAD
    ages = []     
=======

    tag = "INFORMATION"
    concerned = "INDIVIDUAL"
    name = "US27"
    description = "List each individual's age"

    #ssages = []     
>>>>>>> 8bf1f2cf236fab60219dfa6bc1d20368a7e6adf8
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

<<<<<<< HEAD
        ages.append(age)
        individualList[indi].setAge(age)
=======
        #ages.append(age)
        individualList[indi].setAge(age)
        errorMessage(tag, concerned, name, description, indi + " - " + str(age))
>>>>>>> 8bf1f2cf236fab60219dfa6bc1d20368a7e6adf8
        """name = individualList[indi].name.split("/")
        firstName = name[0]
        lastName = name[1]
        print  firstName + lastName + ": " + str(age) + " years" """

    # Each individual's current age when listing
<<<<<<< HEAD
    #outputFile = open('Parser_Output.txt', 'w')
    #individualTable.add_column(["Age",ages])
=======
    # outputFile = open('Parser_Output.txt', 'a')
    # individualTable.add_column('Age', ages)
    # outputFile.write("{0:^150}".format(str(individualTable.get_string(fields=['ID','Name','Age']))) + '\n')
>>>>>>> 8bf1f2cf236fab60219dfa6bc1d20368a7e6adf8

#########################################################################################################################################################################
def checkBigamy(individualList, familyList):
    """ US11 : No bigamy """

    tag = "ERROR"
    concerned = "INDIVIDUAL"
    name = "US11"
    description = "Bigamy has been detected"

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
                                #bigamy = True       
                                errorMessage(tag, concerned, name, description, "in " + firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi)
                        elif (individualList[indi].ID == firstMarriage.wife):
                            if (isAlive(individualList[firstMarriage.husband])):
                                #bigamy = True    
                                errorMessage(tag, concerned, name, description, "in " + firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi)
                        
                    # Otherwise check if the person was once invloved in bigamy
                    else:
                        # If the person got divorced from 1st marriage after marrying the 2nd time
                        if (checkDate(secondMarriage.marriage, firstMarriage.divorce)):
                            #bigamy = True
                            errorMessage(tag, concerned, name, description, "in " + firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi)

###########################################################################################################################################################################
def isAlive(person):
    """ Function to check if a person is still alive 
        ** Not a user story """
    if (person.death != 'NA'):
        return False
    else:
        return True

<<<<<<< HEAD
########################################################################################################################################################################
def US09_birthBeforeDeath(individualList, familyList)
    for i in range(len(familyList)):
        father_id = familyList[i][husband]
        mother_id = familyList[i[wife]
    
=======
###########################################################################################################################################################################
def errorMessage(tag, concerned, name, description, location = '-'):
    outputFile = open('Parser_Output.txt', 'a')
    outputFile.write(tag + '\t' + '\t' + concerned + '\t' + '\t' + name + '\t' + '\t' + '\t' + description + '\t' + '\t' + '\t' + '\t' + location + '\n')
    outputFile.close()
>>>>>>> 8bf1f2cf236fab60219dfa6bc1d20368a7e6adf8
