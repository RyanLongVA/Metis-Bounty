### Models ###

import sys
import MySQLdb, pdb
from MySQLdb import Error
import mysqlfunc 


# All the variables for paths

class ByProgramInScopeId:
	def __init__(self, programName):
		conn = mysqlfunc.create_dbConnection()
		cur = conn.cursor()
		self.programName = programName
		self.ScopeIds = []
		# Grab all the InScopeIds based on the programName
		statem = "SELECT domainRangeId FROM InScope WHERE programId LIKE (SELECT programId FROM Programs WHERE name = \'%s\')"%(programName)
		cur.execute(statem)
		for column in cur.fetchall():
			self.ScopeIds.append(int(column[0]))

# is the inScope domain reference based on the InScopeId provided
class InScope:

	def __init__(self, InScopeId):
		# Create the database connection 
		if type(InScopeId) == int:
			conn = mysqlfunc.create_dbConnection()
			cur = conn.cursor()
			# Grab scope text by scope Id
			self.ScopeText = mysqlfunc.domainRangeByrangeId(cur, InScopeId)

# Parsing Tasks 

test = ByProgramInScopeId("Tesla")
print test.ScopeIds