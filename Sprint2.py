##############################################################################################################################
## Sprint 2
###########################################################################################################################################################################
import datetime
from prettytable import PrettyTable
from Functions import writeTableToFile, checkDate, dates_within
from OutputValues import OutputValues


errorTable = PrettyTable()
errorTable.field_names = ['Tag', 'Concerned', 'User Story', 'Description', 'Location/ ID']

outputValues = OutputValues()
outputFile = ""



def sprint2(individualList, familyList):
    print "sprint2"
    
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
        
        
    writeTableToFile(errorTable,"Sprint2")

########################################################################################################################################################################
def birthdayBeforeCurrentDate_us01(birthday):
    global outputValues
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US01", "Birth day "+ birthday+" is before today")
    if birthday == 'NA':
        outputValues.description = "Birthdate is not specified"
        return False
    today = datetime.date.today().strftime("%Y-%m-%d")
    return checkDate(birthday, today)

def deathBeforCurrentDate_us01(death):
    global outputValues
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US01", "Death day "+ death+" is before today")
    today = datetime.date.today().strftime("%Y-%m-%d")
    return  checkDate(death, today)

def marriageBeforCurrentDate_us01(marriage):
    global outputValues
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US01", "Marriage day "+ marriage+" is before today")
    today = datetime.date.today().strftime("%Y-%m-%d")
    return  checkDate(marriage, today)

def divorceBeforCurrentDate_us01(divorce):
    global outputValues
    outputValues = OutputValues("ERROR", "INDIVIDUAL", "US01", "Divorce day "+ divorce+" is before today")
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