from Individual import Individual
from Family import Family
from collections import OrderedDict
from prettytable import PrettyTable

individual = OrderedDict()
family = OrderedDict()

with open("GEDCOM_File.ged") as inputFile:
	for line in inputFile:
		# Split each line into individual elements
		values = line.split()

		#Check if the line is not blank
		if(values):		
			level = values[0]	# LEVEL
			tag = values[1]		# TAG

			spaceSeparator = ['DATE', 'NAME', 'NOTE']
			sep = ''
			if tag in spaceSeparator:
				sep = ' '
			# ARGS is the remaining part 
			args = sep.join(values[2:])

			# Exception 1
			# For INDI and FAM tag is the 3rd element while ARG is the 2nd element 
			if (tag[0] == '@'):
					tag = values[2]
					args = values[1]

			#Check if the tags are valid by checking with basic syntax
			#Add to Individual and Family OrderedDict
			if (level == '0'):
				args = args.strip('@')
				label = args
				if (tag == 'INDI'):
					individual[label] = Individual(args) 
				elif (tag == 'FAM'):
					family[label] = Family(args)
			elif (level == '1'):
				if (tag == 'NAME'):
					individual[label].setName(args)
				elif (tag == 'SEX'):
					individual[label].setSex(args)
				elif (tag == 'BIRT'):
					date = 'birthday'
				elif (tag == 'DEAT'):
					date = 'death'
				elif (tag == 'FAMC'):
					args = args.strip('@')
					individual[label].setChildFamily(args)
				elif (tag == 'FAMS'):
					args = args.strip('@')
					individual[label].setSpouseFamily(args)
				elif (tag == 'HUSB'):
					args = args.strip('@')
					family[label].setHusband(args)
				elif (tag == 'WIFE'):
					args = args.strip('@')
					family[label].setWife(args)
				elif (tag == 'CHIL'):
					args = args.strip('@')
					family[label].setChildren(args)
				elif (tag == 'MARR'):
					date = 'marriage'
				elif (tag == 'DIV'):
					date = 'divorce'

			elif (level == '2') and (tag == 'DATE'):
				if (date == 'birthday'):
					individual[label].setBirthday(args)
				elif (date == 'death'):
					individual[label].setDeath(args)
				elif (date == 'marriage'):
					family[label].setMarriage(args)
				elif (date == 'divorce'):
					family[label].setDivorce(args)

#Output file
outputFile = open('Parser_Output.txt', 'w')

#Create table with the values
individualTable = PrettyTable()
individualTable.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Death', 'Child', 'Spouse']
for indi in individual:
	individualTable.add_row([individual[indi].ID, individual[indi].name, individual[indi].sex, individual[indi].birthday, individual[indi].death, individual[indi].childFamily, individual[indi].spouseFamily])
outputFile.write(str(individualTable) + '\n')

familyTable = PrettyTable()
familyTable.field_names = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']
for fam in family:
	familyTable.add_row([family[fam].ID, family[fam].marriage, family[fam].divorce, family[fam].husband, individual[family[fam].husband].name, family[fam].wife, individual[family[fam].wife].name, family[fam].children])
outputFile.write(str(familyTable))
