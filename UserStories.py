import datetime
from datetime import date
from Parser import individualTable, familyTable
from Functions import checkDate
from prettytable import PrettyTable
from OutputValues import OutputValues

errorTable = PrettyTable()
errorTable.field_names = ['Tag', 'Concerned', 'User Story', 'Description', 'Location/ ID']

outputValues=OutputValues()

def userStories(individualList, familyList):
    
    # Sprint 2 stories:
    # Sprint 3 stories:
    # Sprint 4 stories:

    #Executing Sprint1
    for indi in individualList:
        #print indi.marriage
        if(birthBeforeMarriage_us02(individualList[indi]) is not True):
            errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,indi])
        if(birthBeforeDeath_us03(individualList[indi]) is not True):
            errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,indi])
    
    individualAge_us27(individualList)
    checkBigamy_us11(individualList, familyList)
    
    US12_parents_not_too_old(individualList, familyList)
    marriage_after_14_US10(individualList,familyList)

    birth_Before_Death_of_Parents_US09(individualList, familyList)
    fewer_than_fifteen_siblings_US15(familyList)

    writeTableToFile(individualList, familyList)

########################################################################################################################################################################
def individualAge_us27(individualList):
    """ US27 : Include individual ages """ 
    tag ="ERROR"
    concerned = "INDIVIDUAL"
    name = "US27"
    description = "Birthday not specified"

    ages = []
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
            ages.append(age)
            # errorTable.add_row([tag,concerned,name,description,indi + " - " + str(age)])
        else:
            errorTable.add_row([tag,concerned,name,description,indi])
    individualTable.add_column('Age', ages)
            

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
                                errorTable.add_row([tag,concerned,name,description, firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi])
                            
                            # Otherwise if the spouse has died his/ her death date
                            else:
                                if (checkDate(secondMarriage.marriage, individualList[firstMarriage.wife].death)):
                                    #bigamy = True
                                    errorTable.add_row([tag,concerned,name,description, firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi])

                        elif (individualList[indi].ID == firstMarriage.wife):
                            if (isAlive(individualList[firstMarriage.husband])):
                                #bigamy = True    
                                errorTable.add_row([tag,concerned,name,description, firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi])
                            else:
                                if (checkDate(secondMarriage.marriage, individualList[firstMarriage.husband].death)):
                                    #bigamy = True
                                    errorTable.add_row([tag,concerned,name,description, firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi])
                    else:
                        # If the person got divorced from 1st marriage after marrying the 2nd time
                        if (checkDate(secondMarriage.marriage, firstMarriage.divorce)):
                            #bigamy = True
                            errorTable.add_row([tag,concerned,name,description, firstMarriage.ID + " and " + secondMarriage.ID + " by " + indi])

###########################################################################################################################################################################
def birthBeforeMarriage_us02(individual):
    global outputValues
    outputValues=OutputValues("ERROR","INDIVIDUAL","US02","marriage "+ individual.marriage+" is before dirthdate "+individual.birthday)
    if individual.marriage=='NA' and individual.birthday != 'NA':
		return True
    if individual.birthday == 'NA':
        outputValues.description="birthdate not specified"
        return False
    return checkDate( individual.birthday, individual.marriage)
    
###########################################################################################################################################################################	
def birthBeforeDeath_us03(individual):
    global outputValues
    outputValues=OutputValues("ERROR","INDIVIDUAL","US03","death "+ individual.death+" is before dirthdate "+individual.birthday)
    if individual.death=='NA' and individual.birthday != 'NA':
		return True
    if individual.birthday == 'NA':
        outputValues.description="birthdate not specified"
        return False
    return checkDate( individual.birthday, individual.death)
	
########################################################################################################################################################################
def birth_Before_Death_of_Parents_US09(individualList, familyList):
        tag="ERROR"
        concerned="FAMILY"
        US="US09"
        description="Death date can't be before Child's"
        location=""
        for x in familyList:
            father_id = familyList[x].husband
            mother_id = familyList[x].wife
            child_type_check = familyList[x].children  
            father_death_date = None
            mother_death_date = None                                     # If only One child then it contains ID's else for checking the type (List or None)
            if type(child_type_check) is None:                                               # If there are no child, No Error
                pass
            elif(type(child_type_check) is list):                                            # if there are multiple children
                            for z in range(len(child_type_check)):
                                    current_child_id = child_type_check[z]                                                                          # Getting the id or current child
                                    for i in individualList:                                       # Looping throug all person dictionary to match the IDs and extract birth and date date
                                            if(individualList[i].ID == father_id):
                                                    father_death_date = individualList[i].death
                                            if(individualList[i].ID == mother_id):
                                                    mother_death_date = individualList[i].death
                                                    
                                            if(individualList[i].ID == current_child_id):
                                                    child_birth_date = individualList[i].birthday
                                                   


                                                    if(father_death_date and mother_death_date is not None):                        # If both parents have a death date
                                                            if(father_death_date is not None and father_death_date > child_birth_date):   # If father has a deathddate and its after the childbirth date
                                                                    pass
                                                            else:
                                                                errorTable.add_row([tag,concerned,US,description,father_id + '-'+ current_child_id])

                                                            if(mother_death_date is not None and mother_death_date > child_birth_date):   # If mother has a deathdate and its after the childBirth Date
                                                                    pass
                                                            else:
                                                                errorTable.add_row([tag,concerned,US,description,mother_id+ '-' +current_child_id])

            else:                                                                                               # If there is only one child, take child_type_check as ID 
                            for i in individualList:
                                    if(individualList[i].ID == father_id):                                    # Getting dates
                                            father_death_date = individualList[i].death
                                    if(individualList[i].ID== mother_id):
                                            mother_death_date = individualList[i].death
                                    if(individualList[i].ID == child_type_check):
                                            child_birth_date = individualList[i].birthday

                                            if(father_death_date and mother_death_date is not None):                # Same check as above
                                                    if(father_death_date is not None and father_death_date > child_birth_date):
                                                            pass
                                                    else:
                                                        errorTable.add_row([tag,concerned,US,description,father_id + '-'+ child_type_check])

                                                    if(mother_death_date is not None and mother_death_date > child_birth_date):
                                                            pass  
                                                    else:
                                                        errorTable.add_row([tag,concerned,US,description,mother_id+ '-' +child_type_check])
 
#########################################################################################################################################################################    
def fewer_than_fifteen_siblings_US15(familyList):
        tag="ERROR"
        concerned="FAMILY"
        US="US15"
        description="Fewer than 15 siblings"
        location=""
	for i in familyList:
		if familyList[i].children != None and len(familyList[i].children) >= 15:
                    errorTable.add_row([tag,concerned,US,description,familyList[i].ID])
			#print "ERROR: FAMILY: US15: Fewer than 15 siblings  Violated - For id "+ family.ID
		    return False
	return True

#########################################################################################################################################################################
def US12_parents_not_too_old(individualList, familyList):
    tag="ERROR"
    concerned="INDIVIDUAL"
    US="US12"
    description="Parents not too old"
    location=""
        
    for i in familyList:
        if familyList[i].children != None:
            father_id = familyList[i].husband
            mother_id = familyList[i].wife
            child_id = familyList[i].children
             
            father_age = individualList[father_id].age
            mother_age = individualList[mother_id].age
            for a in range(len(child_id)):                                   
                child_age = individualList[child_id[a]].age
                                     
                			
                if ((father_age - child_age > 80) or (mother_age - child_age > 60)):
                    errorTable.add_row([tag,concerned, US, description, father_id + '-' + mother_id])
                    


##########################################################################################################################################################################
def marriage_after_14_US10(individualList,familyList):
    tag="ANAMOLY"
    concerned="INDIVIDUAL"
    US="US10"
    description="Marraige should be after 14 years of birth "
    location=""
    for i in familyList:
        husband_id = familyList[i].husband
        wife_id = familyList[i].wife
        Marraige_date = familyList[i].marriage
        #print Marraige_date
        birth = familyList[i].marriage.split("-")
        m_year = int(birth[0])
        #print m_year
        for z in individualList:
            if individualList[z].ID == husband_id:
                birth = individualList[z].birthday.split("-")
                h_year = int(birth[0])
                #print h_year
            if individualList[z].ID == wife_id:
                birth = individualList[z].birthday.split("-")
                w_year = int(birth[0])
                #print w_year
        if m_year - h_year >= 14 and m_year - w_year >=14:
            pass
        else:
            errorTable.add_row([tag,concerned, US, description, husband_id + '-' + wife_id])

###########################################################################################################################################################################
def writeTableToFile(individualList, familyList):
    # Output file
    outputFile = open('Parser_Output.txt', 'w')    
    outputFile.write(str(individualTable) + '\n\n')
    outputFile.write(str(familyTable) + '\n\n')

    outputFile.write('\n\n'  + "{0:^150}".format(" Error Report") + "\n\n")
    outputFile.write(str(errorTable)+"\n")
    outputFile.close()

###########################################################################################################################################################################
def isAlive(person):
    """ Function to check if a person is still alive
        ** Not a user story """
    if (person.death != 'NA'):
        return False
    else:
        return True

###########################################################################################################################################################################