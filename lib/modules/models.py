### Models ###

import sys
import MySQLdb, pdb
from MySQLdb import Error
import mysqlfunc 


# All the variables for paths

class InScopeIdsByAll:
	def __init__(self):
		conn = mysqlfunc.create_dbConnection()
		cur = conn.cursor()
		# Saving the programI
		self.ScopeIds = []
		# Grab all the InScopeIds based on the programName
		statem = "SELECT domainRangeId FROM InScope"
		cur.execute(statem)
		for column in cur.fetchall():
			self.ScopeIds.append(int(column[0]))
		if len(self.ScopeIds) is 0:
			print '[-] There were no domainRangeIds in InScope'
			print '[-] Exiting'
			exit()

class InScopeIdsByProgram:
	def __init__(self, programName):
		conn = mysqlfunc.create_dbConnection()
		cur = conn.cursor()
		# Saving the programI
		self.ScopeIds = []
		# Grab all the InScopeIds based on the programName
		statem = "SELECT domainRangeId FROM InScope WHERE programId LIKE (SELECT programId FROM Programs WHERE name = \'%s\')"%(programName)
		cur.execute(statem)
		for column in cur.fetchall():
			self.ScopeIds.append(int(column[0]))
		if len(self.ScopeIds) is 0:
			print '[-] The program',programName,'didn\'t exist or had no InScopeId'
			print '[-] Exiting'
			exit()

# is the inScope domain reference based on the InScopeId provided
class InScope:

	def __init__(self, InScopeId, programId = None):
		# Create the database connection 
		if type(InScopeId) == int:
			conn = mysqlfunc.create_dbConnection()
			cur = conn.cursor()
			# Keep the Id for safe keeping
			self.InScopeId = InScopeId
			# Grab scope text by scope Id
			self.ScopeText = mysqlfunc.domainRangeByrangeId(cur, InScopeId)
			# Saving the programId within the class
			if programId is None:
				# Select it from the database by the InScopeId
				statem =  "SELECT programId FROM InScope WHERE domainRangeId = %s"%(InScopeId)
				cur.execute(statem)
				self.ProgramId = int(cur.fetchone()[0])
			else:
				self.ProgramId = programId
		else: 
			print '[-] The provided InScopeId {{',InScopeId,'}} was not a int'
			print '[-] Exiting...'
			exit()

# RulesDomain
# -- Model for each domain within the rules engine

class RulesDomain:

	def __init__(self, DomainName, DomainId, InScopeId, ProgramId):
		self.DomainName = DomainName
		self.DomainId = DomainId
		self.InScopeId = InScopeId
		self.ProgramId = ProgramId

# Quick dict for scope types
ScopeTypes = {
	1 : 'asns',
	2 : 'inScopeText'
}

# Parsing Tasks 

Tasks = {
	'Subfinder': 
		{ 'function': 'Subfinder', 'type' : 'inScopeText' },
	'Crtsh':
		{ 'function': 'Subfinder', 'type' : 'inScopeText'},
	'Amass':
		{ 'function': 'Amass', 'type' : 'inScopeText'},
	'Gobuster':
		{ 'function': 'Gobuster', 'type' : 'inScopeText'},
	'Crtsh':
		{ 'function': 'Crtsh', 'type' : 'inScopeText'}
}

#class TasksQueue:
	# Parsing object tasks
	#def __init__(self, TaskListString):
