from Functions import formatDate

class Family(object):
	
	def __init__(self, ID = 'NA', husband = 'NA', wife = 'NA', marriage = 'NA', divorce = 'NA'):
		self.ID = ID
		self.husband = husband
		self.wife = wife
		self.children = []
		self.marriage = marriage
		self.divorce = divorce

	def setHusband(self, husband):
		self.husband = husband

	def setWife(self, wife):
		self.wife = wife

	def setChildren(self, child):
		self.children.append(child)

	def setMarriage(self, marriage):
		marriage = formatDate(marriage)
		self.marriage = marriage

	def setDivorce(self, divorce):
		divorce = formatDate(divorce)
		self.divorce = divorce
	
	def getHusband(self):
		return self.husband

	def getWife(self):
		return self.wife
