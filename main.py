#################################################################
##				   	       MAIN FILE	   					   ##
#################################################################

from Parser import parser, individual, family
from UserStories import userStories

parser()

# Pass in the individual and family lists for the user-story validations
userStories(individual, family)
