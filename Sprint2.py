##############################################################################################################################
## Sprint 2
###########################################################################################################################################################################
import datetime
from prettytable import PrettyTable
from Functions import writeTableToFile, checkDate, dates_within
from OutputValues import OutputValues
from Sprint1 import determineSpouse,isAlive


errorTable = PrettyTable()
errorTable.field_names = ['Tag', 'Concerned', 'User Story', 'Description', 'Location/ ID']

outputValues = OutputValues()
outputFile = ""

def sprint2(individualList, familyList):
    print "sprint2"
    previousIndividual = []
    previousSiblings = []
    
    for indi in individualList:
        #Executing Sprint2
        if birthdayBeforeCurrentDate_us01(individualList[indi].birthday) is not True:
            errorTable.add_row([outputValues.tag, outputValues.concerned, outputValues.US, outputValues.description, indi])
        if deathBeforCurrentDate_us01(individualList[indi].death) is not True:
            errorTable.add_row([outputValues.tag, outputValues.concerned, outputValues.US, outputValues.description, indi])
        if marriageBeforCurrentDate_us01(individualList[indi].marriage) is not True:
            errorTable.add_row([outputValues.tag, outputValues.concerned, outputValues.US, outputValues.description, indi])
        if divorceBeforCurrentDate_us01(individualList[indi].divorce) is not True:
            errorTable.add_row([outputValues.tag, outputValues.concerned, outputValues.US, outputValues.description, indi])
        if lessThan150Years_US07(individualList[indi]) is not True:
            errorTable.add_row([outputValues.tag, outputValues.concerned, outputValues.US, outputValues.description, indi])

        #user story 21 and 29
        if correct_gender_for_role_US21(individualList[indi], familyList) is not True:
            for location in outputValues.location:
                errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])
        if list_of_deceased_US29(individualList[indi]) is not True:
            for location in outputValues.location:
                errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])


        individual = individualList[indi]
        # User story 17
        if (marriedToDescendants_us17(individual, individualList, familyList)):
            for location in outputValues.location:
               errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location]) 
        # User story 18
        if (marriedToSiblings_us18(individual, familyList)):          
            for location in outputValues.location:
                if (indi not in previousSiblings or location.split("-")[1] not in previousIndividual):
                    previousSiblings.append(location.split("-")[1])
                    errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])
            previousIndividual.append(indi)
                
    writeTableToFile(errorTable,"Sprint2")

########################################################################################################################################################################
def birthdayBeforeCurrentDate_us01(birthday):
    global outputValues
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US01", "Birth day "+ birthday+" is after today")
    if birthday == 'NA':
        outputValues.description = "Birthdate is not specified"
        return False
    today = datetime.date.today().strftime("%Y-%m-%d")
    return checkDate(birthday, today)

def deathBeforCurrentDate_us01(death):
    global outputValues
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US01", "Death day "+ death+" is after today")
    today = datetime.date.today().strftime("%Y-%m-%d")
    return  checkDate(death, today)

def marriageBeforCurrentDate_us01(marriage):
    global outputValues
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US01", "Marriage day "+ marriage+" is after today")
    today = datetime.date.today().strftime("%Y-%m-%d")
    return  checkDate(marriage, today)

def divorceBeforCurrentDate_us01(divorce):
    global outputValues
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US01", "Divorce day "+ divorce+" is after today")
    today = datetime.date.today().strftime("%Y-%m-%d")
    return checkDate(divorce, today)

########################################################################################################################################################################
def lessThan150Years_US07(individual):
    global outputValues
    outputValues=OutputValues("ERROR","INDIVIDUAL","US07","Individual's age is more than 150 years")
    if individual.birthday!= 'NA':
        if individual.death!='NA':
            return dates_within(individual.birthday, individual.death, 150, 'years')
        else:
            return dates_within(individual.birthday, datetime.date.today().strftime("%Y-%m-%d"), 150, 'years')
    return False

###########################################################################################################################################################################
def marriedToDescendants_us17(individual, individualList, familyList):
    """ US18 : Siblings should not marry each other """
    global outputValues
    error = False
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US17", "Parent married to its descendant")
    outputValues.location = []
    spouses = set()
    children = set()
    grandChildren = set()
    descendants = set()
    # For each married individual having children
    if (individual.spouseFamily != 'NA'):
        family = familyList[individual.spouseFamily]
        spouses.add(determineSpouse(individual, family))
        if (family.children):
            children = set(family.children)
            # Collect all its spouses and children
            for fam in familyList:
                if (fam != family.ID and (individual.ID == familyList[fam].husband or individual.ID == familyList[fam].wife)):
                    spouses.add(determineSpouse(individual, familyList[fam]))
                    children.update(familyList[fam].children)
            
            # Now collect the grand children
            for child in children:
                childObj = individualList[child]
                if (childObj.spouseFamily != 'NA'):
                    family2 = familyList[childObj.spouseFamily]
                    if (family2.children):
                        grandChildren.update(family2.children)
                        for fam2 in familyList:
                            if (fam2 != family2.ID and (childObj.ID == familyList[fam2].husband 
                                or childObj.ID == familyList[fam2].wife)):
                                grandChildren.update(familyList[fam2].children)

            # Combine the children and grand children of an individual as its descendants
            descendants = children.union(grandChildren)
            spouses.intersection_update(descendants)
            # Check if any of its spouses is its descendant also
            if (len(spouses) != 0):
                error = True
                for spouse in spouses:
                    outputValues.location.append(individual.ID + "-" + spouse)        
    return error
    
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
        # Consider all the half siblings (i.e. children of the individual's parents)
        for fam in familyList:
            if (fam != family.ID and (familyList[fam].husband == family.husband or familyList[fam].wife == family.wife)):
                siblings.update(familyList[fam].children)
        # For the individual in question check all its spouses and see if any of them is a sibling
        for fam2 in familyList:
            family2 = familyList[fam2]
            if (individual.spouseFamily == family2.ID or individual.ID == family2.husband or individual.ID == family2.wife):
                spouse = determineSpouse(individual, family2)
                if (spouse in siblings):
                    error = True
                    outputValues.location.append(individual.ID + "-" + spouse)
    return error

###########################################################################################################################################################################
def correct_gender_for_role_US21(individualList, familyList):
        global outputValues
        outputValues = OutputValues("ERROR", "FAMILY", "US21")
        outputValues.location = []
	for i in familyList:
		husband_id = familyList[i].husband
		wife_id = familyList[i].wife

		#for i in individualList:
		if individualList.ID == husband_id:
				if individualList.sex == 'M':
					continue
                                        return True
				else:
                                        outputValues.location.append(individualList.ID)
                                        outputValues.description="Correct gender for role is violated for husband_id"
                                        return False
                if individualList.ID == wife_id:
				if individualList.sex == 'F':
					continue
                                        return True
				else:
                                        outputValues.location.append(individualList.ID)
                                        outputValues.description="Correct gender for role is violated for wife_id"
                                        return False
#######################################################################################################################################################################
def list_of_deceased_US29(individualList):
        global outputValues
        outputValues = OutputValues("ERROR", "INDIVIDUAL", "US29","Deceased people")
        outputValues.location = []
	#for i in individualList:
	#individual_ID = individualList[i].ID
	if(isAlive(individualList)) is not True:
            outputValues.location.append(individualList.ID)
            return False
