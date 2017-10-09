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

    ages = []
    previousIndividual = []
    previousSiblings = []

    for indi in individualList:
        #Executing Sprint1
        if(birthBeforeMarriage_us02(individualList[indi]) is not True):
            errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,indi])
        if(birthBeforeDeath_us03(individualList[indi]) is not True):
            errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,indi])

        individual = individualList[indi]
        # User story 27:
        age = individualAge_us27(individual)
        individual.setAge(age)
        ages.append(age)
        # User story 11:
        if (checkBigamy_us11(individual, individualList, familyList)):
            errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,outputValues.location])


        #Executing Sprint2
        # User story 17
        # if (marriedToDescendants_us17(individual, familyList)):
        # User story 18
        if (marriedToSiblings_us18(individual, familyList)):
            print outputValues.location           
            for location in outputValues.location:
                if (indi not in previousSiblings or location.split(",")[1] not in previousIndividual):
                    previousSiblings.append(location.split(",")[1])
                    errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])
            previousIndividual.append(indi)
                 
    individualTable.add_column('Age', ages)
       
    US12_parents_not_too_old(individualList, familyList)
    marriage_after_14_US10(individualList,familyList)

    birth_Before_Death_of_Parents_US09(individualList, familyList)
    fewer_than_fifteen_siblings_US15(familyList)

    writeTableToFile(individualList, familyList)

########################################################################################################################################################################
def individualAge_us27(individual):
    """ US27 : Include individual ages """ 
    if (individual.birthday != 'NA'):
        birth = individual.birthday.split("-")           
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
        return age
    else:
        errorTable.add_row(["ERROR", "INDIVIDUAL", "US27", "Birthdate of " + individual + " not specified"])
        return "NA"
            

#########################################################################################################################################################################
def checkBigamy_us11(individual, individualList, familyList):
    """ US11 : No bigamy """
    global outputValues
    error = False    
    if (individual.spouseFamily != 'NA'):   # Exclude the un-married people
        for fam in familyList:
            family = familyList[fam]
            # Enter only if the person is a spouse in any other family apart from the one he/ she is currently a spouse in.
            if (fam != individual.spouseFamily and ((family.husband and individual.ID == family.husband)
                 or (family.wife and individual.ID == family.wife))):
                if (familyList[individual.spouseFamily].marriage and family.marriage): # If both marriage dates available
                    firstMarriage, secondMarriage = determineMarriageOrder(familyList[individual.spouseFamily], family)
                    spouseID = determineSpouse(individual, firstMarriage)
                    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US11",
                            "Bigamy has been detected", firstMarriage.ID + "," + secondMarriage.ID + " - " + individual.ID)
                    # Check if the person got married 2nd time even when he/ she has not yet been divorced from the 1st marriage
                    if (firstMarriage.divorce == 'NA'):                                         
                        # Then check if the spouse from the 1st marriage is still alive
                        if (isAlive(individualList[spouseID])):                           
                            error = True                                     
                        # Otherwise check if the spouse died after the second marrriage
                        else:
                            if (checkDate(secondMarriage.marriage, individualList[spouseID].death)):
                                error = True
                    else:
                        # If the person got divorced from 1st marriage after marrying the 2nd time
                        if (checkDate(secondMarriage.marriage, firstMarriage.divorce)):
                            error = True
    return error

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
def marriedToDescendants_us17(individual, familyList):
    """ US18 : Siblings should not marry each other """
    global outputValues
    error = False
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US18", "Parents married to their descendants")
    outputValues.location = []
    if (individual.spouseFamily != 'NA'):
        family = individual.spouseFamily
        # if (family.children):

    
###########################################################################################################################################################################
def marriedToSiblings_us18(individual, familyList):
    """ US18 : Siblings should not marry each other """
    global outputValues
    error = False
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US18", "Siblings of a family are married to each other")
    outputValues.location = []
    siblings = set()
    siblings.add(individual.ID)
    if (individual.childFamily != 'NA' and individual.spouseFamily != 'NA'):
        family = familyList[individual.childFamily]
        siblings.symmetric_difference_update(family.children)
        for fam in familyList:
            if (fam != family.ID and (familyList[fam].husband == family.husband or familyList[fam].wife == family.wife)):
                siblings.update(familyList[fam].children)
        for fam2 in familyList:
            family2 = familyList[fam2]
            if (individual.spouseFamily == family2.ID or individual.ID == family2.husband or individual.ID == family2.wife):
                spouse = determineSpouse(individual, family2)
                if (spouse in siblings):
                    error = True
                    outputValues.location.append(individual.ID + "," + spouse)
    return error

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
def determineMarriageOrder(marriage1, marriage2):
    """ Not a user story """
    if checkDate(marriage1.marriage, marriage2.marriage):
        return marriage1, marriage2
    else:
        return marriage2, marriage1

###########################################################################################################################################################################
def determineSpouse(individual, family):
    """ Not a user story """
    if (individual.ID == family.husband):
        return family.wife 
    else:
        return family.husband

###########################################################################################################################################################################