from datetime import datetime
from datetime import date
from prettytable import PrettyTable
from Functions import writeTableToFile, checkDate, dates_within
from OutputValues import OutputValues

errorTable = PrettyTable()
errorTable.field_names = ['Tag', 'Concerned', 'User Story', 'Description', 'Location/ ID']

outputValues = OutputValues()
outputFile = ""

def sprint4(individualList, familyList):
    print "sprint4"
    
    for indi in individualList:
    	pass

    for fam in familyList:
    	family = familyList[fam]
    	if (correspondingEntries_us26(family, individualList)):
    		for location in outputValues.location:
    			errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,location])

    	orderSiblings_us28(family, individualList)
    	errorTable.add_row([outputValues.tag,outputValues.concerned,outputValues.US,outputValues.description,outputValues.location])   		

    writeTableToFile(errorTable,"Sprint4")

######################################################################################################################################################################
def correspondingEntries_us26(family, individualList):
	global outputValues
	error = False
	outputValues = OutputValues("ERROR", "FAM/INDI", "US26", "Corresponding Entries do not match")
	outputValues.location = []
	husband = family.husband
	wife = family.wife
	if (family.ID != individualList[husband].spouseFamily):
		error = True
		outputValues.location.append(family.ID + "-" + husband)
	if (family.ID != individualList[wife].spouseFamily):
		error = True
		outputValues.location.append(family.ID + "-" + wife)
	for child in family.children:
		if (family.ID != individualList[child].childFamily):
			error = True
			outputValues.location.append(family.ID + "-" + child)
	return error

######################################################################################################################################################################
def orderSiblings_us28(family, individualList):
	global outputValues
	outputValues = OutputValues("ERROR", "INFORMATION", "US28", "Ordered Siblings")
	outputValues.location = "No children"
	if (family.children):
		outputValues.location = family.ID
		children = family.children
		for i in xrange(len(children)-1):
			j = i+1
			if (individualList[children[i]].age <= individualList[children[j]].age):
				temp = children[i]
				children[i] = children[j]
				children[j] = temp
		for child in children:
			outputValues.location = outputValues.location +  " " + child
		return outputValues.location