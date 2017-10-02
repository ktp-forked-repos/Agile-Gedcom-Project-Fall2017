#################################################################
##				   				   							   ##
##					General Purpose Functions				   ##
##															   ##
#################################################################

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
		date1simplified=date1.split("-")
		date2simplified=date2.split("-")
		res= False
		if date1simplified[0]<date2simplified[0]:
			res=True
		if date1simplified[0]==date2simplified[0] and date1simplified[1]<date2simplified[1]:
			res=True
		if date1simplified[0]==date2simplified[0] and date1simplified[1]==date2simplified[1] and date1simplified[2]<=date2simplified[2] :
			res=True
		return res