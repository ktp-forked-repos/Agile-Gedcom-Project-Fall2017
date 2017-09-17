from Functions import formatDate

class Individual(object):

	def __init__(self, ID, name = '', sex = '', birthday = '', death = 'NA', childFamily = 'NA', spouseFamily = 'NA'):
		self.ID = ID
		self.name = name
		self.sex = sex
		self.birthday = birthday
		self.death = death
		self.childFamily = childFamily
		self.spouseFamily = spouseFamily

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

	def setChildFamily(self, childFamily):
		self.childFamily = childFamily

	def setSpouseFamily(self, spouseFamily):
		self.spouseFamily = spouseFamily

		
