from Functions import checkDate
from prettytable import PrettyTable
from OutputValues import OutputValues
from Functions import writeTableToFile
from Parser import individualTable, familyTable
import os
import datetime

errorTable = PrettyTable()
errorTable.field_names = ['Tag', 'Concerned', 'User Story', 'Description', 'Location/ ID']

outputValues = OutputValues()
outputFile = ""


def sprint1(individualList, familyList):
    print "sprint1"
    
    for indi in individualList:
        #Executing Sprint1
        if birthBeforeMarriage_us02(individualList[indi]) is not True:
            errorTable.add_row([outputValues.tag, outputValues.concerned, outputValues.US, outputValues.description, indi])
        if birthBeforeDeath_us03(individualList[indi]) is not True:
            errorTable.add_row([outputValues.tag, outputValues.concerned, outputValues.US, outputValues.description, indi])

        # User story 10
        if marriage_after_14_US10(individualList[indi],familyList) is not True:
            for location in outputValues.location:
                errorTable.add_row([outputValues.tag, outputValues.concerned, outputValues.US, outputValues.description,location])

        individual = individualList[indi]
        # User story 11:
        if (checkBigamy_us11(individual, individualList, familyList)):
            errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,outputValues.location])
               
    #User story 12
    if (US12_parents_not_too_old(individualList, familyList))is not True:
        for location in outputValues.location:
            errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])

    
    #user story 09-15
    birth_Before_Death_of_Parents_US09(individualList, familyList)
    if fewer_than_fifteen_siblings_US15(familyList) is not True:
        errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,outputValues.location])
           
  
    writeTableToFile(errorTable,"Sprint1")            
#########################################################################################################################################################################
"""For Testing Purpose"""
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
            age -= 1
        elif (today.month == birthmonth):
            if (today.day < birthdate):
                age -= 1
        return age

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
    outputValues=OutputValues("ERROR","INDIVIDUAL","US02","marriage "+ individual.marriage+" is before birthdate "+individual.birthday)
    if individual.marriage=='NA' and individual.birthday != 'NA':
		return True
    if individual.birthday == 'NA':
        outputValues.description="birthdate not specified"
        return False
    return checkDate( individual.birthday, individual.marriage)
    
###########################################################################################################################################################################	
def birthBeforeDeath_us03(individual):
    global outputValues
    outputValues=OutputValues("ERROR","INDIVIDUAL","US03","death "+ individual.death+" is before birthdate "+individual.birthday)
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
        global outputValues
        
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
                                    current_child_id = child_type_check[z]
                                    # Getting the id or current child
                                    for i in individualList:                                       # Looping throug all person dictionary to match the IDs and extract birth and date date
                                            if(individualList[i].ID == father_id):
                                                    father_death_date = individualList[i].death
                                            if(individualList[i].ID == mother_id):
                                                    mother_death_date = individualList[i].death
                                                    
                                            if(individualList[i].ID == current_child_id):
                                                    child_birth_date = individualList[i].birthday
                                    
                                    if(father_death_date and mother_death_date is not None):
                                         if(father_death_date > child_birth_date):   # If father has a deathddate and its after the childbirth date
                                              pass
                                         else:
                                              errorTable.add_row([tag,concerned,US,description,father_id + '-'+ current_child_id])
                                         if(mother_death_date > child_birth_date):
                                              pass
                                         else:
                                               errorTable.add_row([tag,concerned,US,description,mother_id+ '-' +current_child_id])
                                                                    
            else:
                for i in individualList:
                                    if(individualList[i].ID == father_id):                                    # Getting dates
                                            father_death_date = individualList[i].death
                                    if(individualList[i].ID== mother_id):
                                            mother_death_date = individualList[i].death
                                    if(individualList[i].ID == child_type_check):
                                            child_birth_date = individualList[i].birthday

                                            if(father_death_date and mother_death_date is not None):                # Same check as above
            

                                                    if( father_death_date > child_birth_date):
                                                            pass
                                                    else:
                                                        
                                                        errorTable.add_row([tag,concerned,US,description,father_id + '-'+ child_type_check])
                                                    

                                                    if( mother_death_date > child_birth_date):
                                                            pass  
                                                    else:
                                                       
                                                        errorTable.add_row([tag,concerned,US,description,mother_id+ '-' +child_type_check])           
       
#########################################################################################################################################################################    
def fewer_than_fifteen_siblings_US15(familyList):
        global outputValues
        outputValues = OutputValues("ERROR", "FAMILY", "US15", "Fewer than 15 siblings" )
        outputValues.location =[]
	for i in familyList:
		if familyList[i].children != None and len(familyList[i].children) >= 15:
                    outputValues.location = familyList[i].ID
		    return False
	return True


#########################################################################################################################################################################
def US12_parents_not_too_old(individualList, familyList):
    global outputValues
    outputValues = OutputValues("ANAMOLY","INDIVIDUAL","US12"," Parents too old ")
    outputValues.location=[]
            
    for i in familyList:
        if familyList[i].children != None:
            father_id = familyList[i].husband
            mother_id = familyList[i].wife
            #print mother_id
            child_id = familyList[i].children
            father_age = individualList[father_id].age
            mother_age =individualList[mother_id].age
            #print mother_age

        for a in range(len(child_id)):
            #for i in individualList:
            
                #child_new_id = child_id[a]
                        #print child_new_id
                #if (individualList[i].ID  == child_new_id):
            child_age = individualList[child_id[a]].age
                    #print child_age
##
##                if individualList[i].ID == father_id:
##                    father_age = individualList[i].age
##                        
##                    
##                if individualList[i].ID == mother_id:
##                    mother_age =individualList[i].age
                        
            if (father_age - child_age) > 80:
                outputValues.location.append(father_id)
                return False
            if (mother_age - child_age) > 60:
                outputValues.location.append(mother_id)
                return False
            
##########################################################################################################################################################################
def marriage_after_14_US10(individualList,familyList):
    global outputValues
    outputValues = OutputValues("ANAMOLY","INDIVIDUAL","US10"," Marraige before 14 years of age ")  
    outputValues.location=[]
  
   
    for i in familyList:
        husband_id = familyList[i].husband
        wife_id = familyList[i].wife
        if familyList[i].marriage != 'NA':
            Marraige_date = familyList[i].marriage
            birth = familyList[i].marriage.split("-")
            m_year = int(birth[0])
                      
        if individualList.ID == husband_id:
            birth = individualList.birthday.split("-")
            h_year = int(birth[0])
            if (m_year - h_year >= 14):
                pass
            #return True
            else:
                outputValues.location.append(husband_id)       
                return False
                

        if individualList.ID == wife_id:
            birth = individualList.birthday.split("-")
            w_year = int(birth[0])
            if (m_year - w_year >=14):
                pass
            else:
                outputValues.location.append(wife_id)
                return False

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
