### Models ###

import sys
import MySQLdb, pdb
from MySQLdb import Error
import mysqlfunc 
# All the variables for paths



# is the inScope domain reference based on the InScopeId provided
class InScope:

	def __init__(self, InScopeId):
		# Create the database connection 
		if type(InScopeId) == int:
			conn = mysqlfunc.create_dbConnection()
			cur = conn.cursor()
			# Grab scope text by scope Id
			self.ScopeText = mysqlfunc.domainRangeByrangeId(cur, InScopeId) 