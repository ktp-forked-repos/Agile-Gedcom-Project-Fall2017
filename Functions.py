#################################################################
##				   				   							   ##
##					General Purpose Functions				   ##
##															   ##
#################################################################
from datetime import date
from datetime import time
from datetime import datetime

def formatDate(date):
		months = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
		date = date.split()
		if int(date[0]) in xrange(1,10):
			day = '0' + date[0]
		else:
			day = date[0]
		month = months[date[1]]
		year = date[2]

		return (year + '-' + month + '-' + day)


def checkDate(date1, date2):
	if date1 == 'NA':
		return True
	dateTime1 = datetime.strptime(date1, "%Y-%m-%d")
	dateTime2 = datetime.strptime(date2, "%Y-%m-%d")
	return dateTime1.date() < dateTime2.date()

def writeTableToFile(table,sprint):
    # Output file
    outputFile = open("Parser_Output.txt", 'a+')    
    outputFile.write('\n\n'  + "{0:^150}".format(" Error Report for "+sprint) + "\n\n")
    outputFile.write(str(table)+"\n")
    outputFile.close()

def dates_within(date1, date2, limit, units):
	#return True if dt1 and dt2 are within limit units,
	# where:dt1, dt2 are instances of datetimelimit is a numberunits is a string in 
	#('days', 'months', 'years')'''
	dateTime1 = datetime.strptime(date1, "%Y-%m-%d")
	dateTime2 = datetime.strptime(date2, "%Y-%m-%d")
	if units == 'days':
		return abs((dateTime1 -dateTime2).days) <= limit
	elif units == 'months':
		return (abs((dateTime1 -dateTime2).days) / 30.4) <= limit
	elif units == 'years':
		return (abs((dateTime1 -dateTime2).days) / 365.25) <= limit