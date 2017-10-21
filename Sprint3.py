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

    #User stories US30-35
    for indi in individualList:

         if List_living_married_US30(individualList[indi],familyList) is not True:
             for location in outputValues.location:
                 errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])

         if List_recent_births_US35(individualList[indi]) is not True:
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
            
        
          
            
            
