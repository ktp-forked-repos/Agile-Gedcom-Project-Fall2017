from Functions import formatDate
from Functions import checkDate

class Individual(object):

	def __init__(self, ID, name = '', sex = '', birthday = 'NA', death = 'NA', age = '-', childFamily = 'NA', spouseFamily = 'NA'
				,marriage ='NA', divorce='NA'):
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
		marriage= formatDate(marriage)
		self.marriage = marriage

	def setDivorce(self,divorce):
		divorce=formatDate(divorce)
		self.divorce= divorce

	def getBirthday(self):
		return self.birthday

	def getMarriage(self):
		return self.marriage

	def getDeath(self):
		return self.death

	def getDivorce(self):
		return self.divorce
		
