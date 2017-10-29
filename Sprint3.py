from datetime import datetime
from datetime import date
from prettytable import PrettyTable
from Functions import writeTableToFile, checkDate, dates_within
from OutputValues import OutputValues
from Sprint1 import determineSpouse,isAlive


errorTable = PrettyTable()
errorTable.field_names = ['Tag', 'Concerned', 'User Story', 'Description', 'Location/ ID']

outputValues = OutputValues()
outputFile = ""

def sprint3(individualList, familyList):
    print "sprint3"
    previousIndividual = []
    previousSiblings = []
    
    for indi in individualList:
        #User stories US30-35
        if List_living_married_US30(individualList[indi],familyList) is not True:
            for location in outputValues.location:
                errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])

        if List_recent_births_US35(individualList[indi]) is not True:
            for location in outputValues.location:
                errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])

        individual = individualList[indi]
        #User story 19
        if (firstCousinsMarried_us19(individual, individualList, familyList)):
            for location in outputValues.location:
                if (indi not in previousSiblings or location.split("-")[1] not in previousIndividual):
                    previousSiblings.append(location.split("-")[1])
                    errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])
            previousIndividual.append(indi) 

    #User story 13
    for fam in familyList:
        family = familyList[fam]
        if siblingSpacing_us13(family, individualList):
            for location in outputValues.location:
                errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])

    writeTableToFile(errorTable,"Sprint3")

def List_living_married_US30(individualList,familyList):
    global outputValues
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US30")
    outputValues.location = []

    if(isAlive(individualList)) is True:
        for i in familyList:
            husband_id= familyList[i].husband
            wife_id= familyList[i].wife
            if (individualList.ID == husband_id):
                outputValues.location.append(individualList.ID)
                outputValues.description="List of husband Living married"
                return False
            if (individualList.ID == wife_id):
                outputValues.location.append(individualList.ID)
                outputValues.description="List of wife Living married"
                return False


def List_recent_births_US35(individualList):
    global outputValues
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US35","List of recent birth")
    outputValues.location = []
    
    if individualList.birthday != 'NA':
        birthdate = individualList.birthday
        today = date.today().strftime("%Y-%m-%d")
        #print today
        
        d1 = datetime.strptime(birthdate, "%Y-%m-%d")
        d2 = datetime.strptime(today, "%Y-%m-%d")

        recent_birth = (d2 - d1)
        #print recent_birth
        
        #Function to find did the person die withinlast 30days 
        if recent_birth.days < 30 and recent_birth.days > 0:
            outputValues.location.append(individualList.ID)
            #return False


####################################################################################################################################################################
def US37_Spouses_Descendants_died_within_last_30_days(individualList,familyList):
	spouse_descendants = []
	died_within_last_30_days = []
	alive_descendats = []
	for i in all_persons:
		if(isAlive(individualList)) is not True:
			death_date = (person['deathdate'].date() - today.date())            
			if death_date.days < 0 : print "ERROR: Age cannot be LESS than 0"                        
			if death_date.days < 30:
				died_within_last_30_days.append(person['id'])
				
	for died in died_within_last_30_days:
		for family in all_families:
			if died in family['wife_id']:
				spouse_descendants.append(family['husband_id'])
				if family['child'] != None:                
					spouse_descendants.append(family['child'])
			if died in family['husband_id']:
				spouse_descendants.append(family['wife_id'])
				if family['child'] != None:                
					spouse_descendants.append(family['child'])
					
	for alive in spouse_descendants:
		for individual in all_persons:
			if alive == individual['id']:
				if individual['alive'] == True: 
					alive_descendats.append(individual['id'])
	
	print "US 37: List all living spouses and descendants of people in a GEDCOM file who died in the last 30 days are" + ' ' + ', '.join(alive_descendats)
	return alive_descendats

####################################################################################################################################################################
def siblingSpacing_us13(family, individualList):
    global outputValues
    error = False
    outputValues = OutputValues("ERROR", "FAMILY", "US13", "Sibling spacing violated")
    outputValues.location = []
    previousSiblings = []
    if (family.children):
        for child1 in family.children:
            for child2 in family.children:
                if ((child1 != child2) and ((child1 not in previousSiblings) or (child1 not in previousSiblings))):
                    if (moreThan1day(individualList[child1].birthday, individualList[child2].birthday)):
                        previousSiblings.append(child1)
                        previousSiblings.append(child2)
                        outputValues.location.append(family.ID + "-" + child1 + "," + child2)
                        error = True
                    elif (lessThan8Months(individualList[child1].birthday, individualList[child2].birthday)):
                        previousSiblings.append(child1)
                        previousSiblings.append(child2)
                        outputValues.location.append(family.ID + "-" + child1 + "," + child2)
                        error = True
                    
    return error

def lessThan8Months(birthdate1, birthdate2):
    born1 = datetime.strptime(birthdate1, "%Y-%m-%d")
    born2 = datetime.strptime(birthdate2, "%Y-%m-%d")
    months = abs((born1.year - born2.year) * 12 + (born1.month - born2.month))
    if (months < 8):
        return True
    return False

def moreThan1day(birthdate1, birthdate2):
    born1 = datetime.strptime(birthdate1, "%Y-%m-%d")
    born2 = datetime.strptime(birthdate2, "%Y-%m-%d")
    if ((born1.year - born2.year) == 0 and (born1.month - born2.month) == 0):
        days = abs(born1.day - born2.day) 
        if (days > 1):
            return True
    return False
        
####################################################################################################################################################################
def firstCousinsMarried_us19(individual, individualList, familyList):
    global outputValues
    error = False
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US19", "First cousins married to each other")
    outputValues.location = []   
    if (individual.childFamily != 'NA' and individual.spouseFamily != 'NA'):
        father = individualList[familyList[individual.childFamily].husband]
        mother = individualList[familyList[individual.childFamily].wife]
        fatherSiblings = determineSiblings(father, familyList)
        motherSiblings = determineSiblings(mother, familyList)
        UncleAunts = fatherSiblings.union(motherSiblings)
        cousins = []
        for person in UncleAunts:
            cousins.extend(determineChildren(individualList[person], familyList))
        for fam in familyList:
            if (fam == individual.spouseFamily or (individual.ID == familyList[fam].husband) or (individual.ID == familyList[fam].wife)):
                spouse = determineSpouse(individual,familyList[fam])
                if (spouse in cousins):
                    error = True
                    outputValues.location.append(individual.ID + "-" + spouse)
    return error

def determineSiblings(individual, familyList):
    siblings = set()
    if (individual.childFamily != 'NA'):
        siblings.add(individual.ID)
        siblings.symmetric_difference_update(familyList[individual.childFamily].children)
    return siblings

def determineChildren(individual, familyList):
    children = []
    if (individual.spouseFamily != 'NA'):
        for fam in familyList:
            if (fam == individual.spouseFamily or ((individual.ID == familyList[fam].husband) or (individual.ID == familyList[fam].wife))):
                children.extend(familyList[fam].children)
    return children
