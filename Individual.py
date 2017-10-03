from Functions import formatDate
from Functions import checkDate

class Individual(object):

	def __init__(self, ID, name = '', sex = '', birthday = '', death = 'NA', age = '-', childFamily = 'NA', spouseFamily = 'NA'
				,marriage ='NA'):
		self.ID = ID
		self.name = name
		self.sex = sex
		self.birthday = birthday
		self.death = death
		self.age = age
		self.childFamily = childFamily
		self.spouseFamily = spouseFamily
		self.marriage = marriage

	def setName(self, name):
		self.name = name

	def setSex(self, sex):
		self.sex = sex

	def setBirthday(self, birthday):
		birthday = formatDate(birthday)
		self.birthday = birthday

	def setDeath(self, death):
		death = formatDate(death)
		self.death = death

	def setAge(self, age):
		self.age = age

	def setChildFamily(self, childFamily):
		self.childFamily = childFamily

	def setSpouseFamily(self, spouseFamily):
		self.spouseFamily = spouseFamily

	def setMarriage(self, marriage):
		self.marriage = marriage

	def getBirthday(self):
		return self.birthday


	
	def birthBeforeMarriage(self):
		#print self.birthday
		if self.marriage is None:
			return False
		if self.birthday is None:
			return False
		return checkDate( self.birthday, self.marriage)
	
	def birthBeforeDeath(self):
		print self.birthday
		if self.death == 'NA' and self.birthday != '':
			return True
		if self.birthday == '':
			return False
		return checkDate( self.birthday, self.death)	

	
