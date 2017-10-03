import datetime
from Parser import individualTable, familyTable
from Functions import checkDate
from prettytable import PrettyTable

errorTable = PrettyTable()
errorTable.field_names = ['Tag', 'Concerned', 'User Story', 'Description', 'Location/ ID']

def userStories(individualList, familyList):


    # Sprint 1 stories:
    individualAge_us27(individualList)
    checkBigamy_us11(individualList, familyList)
    birthBeforeMarriage_us02(individualList)
    birthBeforeDeath_us03(individualList)
    writeTableToFile()

########################################################################################################################################################################


def individualAge_us27(individualList):
    """ US27 : Include individual ages """ 
    tag = "INFORMATION"
    concerned = "INDIVIDUAL"
    name = "US27"
    description = "List each individual's age"

    for indi in individualList:
        birth = individualList[indi].birthday.split("-")
        if (individualList[indi].birthday != 'NA'):           
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
            individualList[indi].setAge(age)
            #errorMessage(tag, concerned, name, description, indi + " - " + str(age))
            errorTable.add_row([tag,concerned,name,description,indi + " - " + str(age)])
        else:
            #errorMessage("ERROR" , concerned, name, "Birthday not specified")
            errorTable.add_row(["ERROR",concerned,name,"Birthday not specified","-"])

            

#########################################################################################################################################################################


def checkBigamy_us11(individualList, familyList):
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
                                #errorMessage(tag, concerned, name, description, "in " + firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi)
                                errorTable.add_row([tag,concerned,name,description, firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi])

                        elif (individualList[indi].ID == firstMarriage.wife):
                            if (isAlive(individualList[firstMarriage.husband])):
                                #bigamy = True    
                                #errorMessage(tag, concerned, name, description, "in " + firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi)
                                errorTable.add_row([tag,concerned,name,description, firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi])

                    # Otherwise check if the person was once invloved in bigamy
                    else:
                        # If the person got divorced from 1st marriage after marrying the 2nd time
                        if (checkDate(secondMarriage.marriage, firstMarriage.divorce)):
                            #bigamy = True
                            #errorMessage(tag, concerned, name, description, "in " + firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi)
                            errorTable.add_row([tag,concerned,name,description, firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi])

###########################################################################################################################################################################


def isAlive(person):
    """ Function to check if a person is still alive
        ** Not a user story """
    if (person.death != 'NA'):
        return False
    else:
        return True

###########################################################################################################################################################################



def birthBeforeMarriage_us02(individualList):
    tag="ERROR"
    concerned="INDIVIDUAL"
    US="US02"
    description=""
    location=""
    for indi in individualList:
        #print(" INDI "+indi+ "  marriage: "+marriage +" birth: "+birth)
        birthday= individualList[indi].getBirthday()
        marriage= individualList[indi].getMarriage()
        #print(" INDI "+indi+ "  marriage: "+marriage +" birth: "+birthday)
        if marriage == 'NA' and birthday !='':
            #pass this as it is ok
            continue
        elif birthday == '':
            #log this as error
            description="birthdate not specified"
            errorTable.add_row([tag,concerned,US,description,indi])
            #errorMessage(tag, concerned, US, description, indi)
            continue
        else:
            res=checkDate(birthday,marriage)
            if res!= True:
                #log this as error
                description="marriage "+ marriage+" is before dirthdate "+birthday
                #errorMessage(tag, concerned, US, description, indi)
                errorTable.add_row([tag,concerned,US,description,indi])
                #print("INDI "+indi+" NOT ok for marriage")
	
	
def birthBeforeDeath_us03(individualList):
    tag="ERROR"
    concerned="INDIVIDUAL"
    US="US03"
    description=""
    location=""
    for indi in individualList:
        birthday=individualList[indi].getBirthday()
        death=individualList[indi].getDeath()
        #print(" INDI "+indi+ "  death: "+death +" birth: "+birthday)
        if death == 'NA' and birthday != '':
            #pass this as it is okay
            #print ("INDI "+indi +" ok for death")
            continue
        if birthday == '':
            #log this as error
            #print ("INDI "+indi+" NOT ok for death")
            description="birthdate not specified"
            #errorMessage(tag, concerned, US, description, indi)
            errorTable.add_row([tag,concerned,US,description,indi])
            continue
        else:
            res=checkDate(birthday,death)
            if res!= True:
                #log this as error
                #print ("INDI "+ indi+" NOT ok for death")
                description="death "+ death+" is before dirthdate "+birthday
                #errorMessage(tag, concerned, US, description, indi)
                errorTable.add_row([tag,concerned,US,description,indi])
	

########################################################################################################################################################################
    def birth_Before_Death_of_Parents_US09(individualList, familyList):
        for x in range(len(familyList)):
            father_id = familyList[x]['husband']
            mother_id = familyList[x]['wife']
            child_type_check = familyList[x]['child']  
            father_death_date = None
            mother_death_date = None                                     # If only One child then it contains ID's else for checking the type (List or None)
            if type(child_type_check) is None:                                               # If there are no child, No Error
                pass
            elif(type(child_type_check) is list):                                            # if there are multiple children
                            for z in range(len(child_type_check)):
                                    current_child_id = child_type_check[z]                                                                          # Getting the id or current child
                                    for i in range(len(individualList)):                                       # Looping throug all person dictionary to match the IDs and extract birth and date date
                                            if(individualList[i]['id'] == father_id):
                                                    father_death_date = individualList[i]['death']
                                            if(individualList[i]['id'] == mother_id):
                                                    mother_death_date = individualList[i]['death']
                                            if(individualList[i]['id'] == current_child_id):
                                                    child_birth_date = individualList[i]['birthday']

                                                    if(father_death_date and mother_death_date is not None):                        # If both parents have a death date
                                                            if(father_death_date is not None and father_death_date > child_birth_date):   # If father has a deathddate and its after the childbirth date
                                                                    pass
                                                            else:
                                                                    print "ERROR: FAMILY: US09: Violated- Father's (" + father_id + ") Death date can't be before Child's (" + current_child_id + ") Birth Date"
                                                                    print "Father death Date: " + str(father_death_date)
                                                                    print "Child Birth Date: " + str(child_birth_date)
                                                            if(mother_death_date is not None and mother_death_date > child_birth_date):   # If mother has a deathdate and its after the childBirth Date
                                                                    pass  
                                                            else:
                                                                    print "ERROR: FAMILY: US09: Violated- Mother's (" + mother_id + ") Death date can't be before Child's (" + current_child_id + ") Birth Date"
                                                                    print "Mother death Date: " + str(mother_death_date)
                                                                    print "Child Birth Date: " + str(child_birth_date)
            else:                                                                                               # If there is only one child, take child_type_check as ID 
                            for i in range(len(individualList)):
                                    if(individualList[i]['id'] == father_id):                                    # Getting dates
                                            father_death_date = individualList[i]['death']
                                    if(individualList[i]['id'] == mother_id):
                                            mother_death_date = individualList[i]['death']
                                    if(individualList[i]['id'] == child_type_check):
                                            child_birth_date = individualList[i]['birthday']

                                            if(father_death_date and mother_death_date is not None):                # Same check as above
                                                    if(father_death_date is not None and father_death_date > child_birth_date):
                                                            pass
                                                    else:
                                                            print "ERROR: FAMILY: US09: Violated- Father's (" + father_id + ") Death date can't be before Child's (" + child_type_check + ") Birth Date"
                                                            print("Father death Date: " + str(father_death_date))
                                                            print("Child Birth Date: " + str(child_birth_date))
                                                    if(mother_death_date is not None and mother_death_date > child_birth_date):
                                                            pass  
                                                    else:
                                                            print "ERROR: FAMILY: US09: Violated- Mother's (" + mother_id + ") Death date can't be before Child's (" + child_type_check + ") Birth Date"
                                                            print("Mother death Date: " + str(mother_death_date))
                                                            print("Child Birth Date: " + str(child_birth_date))
        

###########################################################################################################################################################################
def fewer_than_fifteen_siblings_US15(familyList):
	for family in familyList:
		if family['child'] != None and len(family['child']) >= 15:
			print "ERROR: FAMILY: US15: Fewer than 15 siblings  Violated - For id "+ family['Family_id']
			return False
	return True

#######################################################################################################################################################################
                
def US09_birthBeforeDeath(individualList, familyList):
    for i in range(len(familyList)):
        father_id = familyList[i][husband]
        mother_id = familyList[i[wife]]
    
   
#########################################################################################################################################################################

def errorMessage(tag, concerned, name, description, location = '-'):
    outputFile = open('Parser_Output.txt', 'a')
    outputFile.write(tag + '\t' + '\t' + concerned + '\t' + '\t' + name + '\t' + '\t' + '\t' + description + '\t' + '\t' + '\t' + '\t' + location + '\n')
    outputFile.close()

def writeTableToFile():
    outputFile = open('Parser_Output.txt', 'a')
    outputFile.write('\n\n'  + "{0:^150}".format(" Error Report") + "\n\n")
    outputFile.write(str(errorTable)+"\n")
    outputFile.close()           
