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

