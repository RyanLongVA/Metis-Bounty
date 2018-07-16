import pdb
# The data models
import models
# The Tasks >> Consists of their runners 
import InScopeTextTasks as InScopeTextTasks
# Import the handy database strings
import mysqlfunc
# Importing the Rules
import ProgramRules, GlobalRules

### Runners ###

class Manager:
	# Manager for when a program is supplied
	def __init__(self, scope, Type, TaskListString):
		self.Type = Type
		self.Tasks = []
		## Check Tasks
		for a in TaskListString.split(','):
			try: 
				self.Tasks.append(models.Tasks[a]) 
			except KeyError: 
				print '[-] Task {',a,'} not found'
				print '[-] Exiting...'
				exit()
			# Check if it's a 
		try:
			if type(int(scope)) == int: 
				# The supplied is a parseable int, so the assumption is it's a domainRangeId
				self.Queue = []
				self.Queue.append(models.InScope(int(scope)))
		except ValueError:
			if type(scope) == str:
				if scope == 'All':
					ReturningIds = models.InScopeIdsByAll()
				else:
					ReturningIds = models.InScopeIdsByProgram(scope) 
				self.Queue = []
				for a in ReturningIds.ScopeIds:
					self.Queue.append(models.InScope(a))
	def Execute(self):
		if self.Type == models.ScopeTypes[2]:
			# InScopeText Tasks
			for ScopeItem in self.Queue:				
				# Make a InScopeWrapper instance and execute
				CurrentScopeWrapper = InScopeTaskWrapper(ScopeItem, self.Tasks) 
				CurrentScopeWrapper.Execute()

# Parsing Arguments
class InScopeTaskWrapper:
	def __init__(self, ScopeItem, TaskArrayOrString):
		if type(TaskArrayOrString) == list:
			# It must be already parsed
			self.Tasks = TaskArrayOrString
		elif type(TaskArrayOrString) == str:
			# It hasn't been parsed
			self.Tasks = []
			for a in TaskListString.split(', '):
				try: 
					self.Tasks.append(models.Tasks[a]) 
				except KeyError: 
					print '[-] Task {',a,'} not found'
					print '[-] Exiting...'
					exit()
		self.ScopeItem = ScopeItem

	def Execute(self):
		# Assumptions: 
		# 	- The only dynamic value is the ScopeText object (which is past in every instance)

		# Iterate over tasks
		for a in self.Tasks:
			# Get the attribute
			print '[+] Executing Task:',a['function']
			getattr(InScopeTextTasks, a['function'])(self.ScopeItem) 		
		# Should do all the work, evne the parsing / sending

class RulesEngineManager:
	def __init__(self, initScopeInput = None, domain = None, OnlyNotCalculated = None):
		self.RulesDomains = []
		self.OnlyNotCalculated = OnlyNotCalculated
		if domain:
			# start based on domain
			self.rulesDomainByDomain(domain)
		elif initScopeInput:
			InScopeIds = []
			if type(initScopeInput) == str:
				# We look the assumed program name (currently) 
				conn = mysqlfunc.create_dbConnection()
				cur = conn.cursor()
				InScopeIds = mysqlfunc.returnInScopeIds(cur, initScopeInput)
			else: 
				# We start based on the inScopeId
				InScopeIds.append(initScopeInput)
			# Use the InScopeId(s) to create the RulesDomain objects and append them to the list
			for curId in InScopeIds: 
				# Creation of the InScope
				curIdObject = models.InScope(curId)
				self.rulesDomainsByInScopeId(curIdObject)

	def Execute(self):
		for curRulesDomain in self.RulesDomains:
			print '[+] Starting on',curRulesDomain.DomainName
			# Run Globals
			curGlobalResults = GlobalRules.Global(curRulesDomain)
			# Run Program depth rules
			if hasattr(ProgramRules, curRulesDomain.ProgramName):
				curProgramResults = getattr(ProgramRules, curRulesDomain.ProgramName)(curRulesDomain)
			else:
				print '\t[!] Warning: Program {%s} Does not have a ProgramRulesEngine'
				curProgramResults = getattr(ProgramRules, 'BlankClass')(curRulesDomain)

			# Set vars: Combine score, Global.Results, Program.Results
			CombinedScore = curGlobalResults.Score + curProgramResults.Score
			# Update in database 
			print '\t RulesScore: %s'%CombinedScore
			print '\t Global: %s'%','.join(curGlobalResults.Results)
			print '\t Program: %s'%','.join(curProgramResults.Results)
			print ''
			statem = "UPDATE Domains SET RulesScore = %s, RulesGlobal = \'%s\', RulesProgram = \'%s\' WHERE domainId = %s"%(CombinedScore, ','.join(curGlobalResults.Results), ','.join(curProgramResults.Results), curRulesDomain.DomainId)
			
			mysqlfunc.sqlExeCommit(statem)		

	def rulesDomainByDomain(self, domain):
		if self.OnlyNotCalculated:
			statem = "SELECT domainName, domainId, domainRangeId FROM Domains WHERE domainName = \'%s\' AND RulesScore IS NULL"%domain
		else:
			statem = "SELECT domainName, domainId, domainRangeId FROM Domains WHERE domainName = \'%s\'"%domain
		result = mysqlfunc.sqlExeRet(statem)
		if len(result) != 1:
			print '  [-] Odd results or no results'
			print '    [*] Info: '+statem
			exit()
		# Log Basics 
		cDomainName = result[0][0]
		cDomainId = result[0][1]
		cDomainRangeId = result[0][2]
		# Grab program id
		statem = "SELECT programId FROM InScope WHERE domainRangeId = %s"%cDomainRangeId
		cProgramId = mysqlfunc.sqlExeRet(statem)[0][0]
		self.RulesDomains.append(models.RulesDomain(cDomainName, cDomainId, cDomainRangeId, cProgramId))

	def rulesDomainsByInScopeId(self, InScopeObject):
		# create the connection and return all the domains 
		if self.OnlyNotCalculated:
			statem = "SELECT domainName, domainId FROM Domains WHERE domainRangeId = %s AND RulesScore IS NULL"%(InScopeObject.InScopeId)
		else:	
			statem = "SELECT domainName, domainId FROM Domains WHERE domainRangeId = %s"%(InScopeObject.InScopeId)
		domainsSqlOut = mysqlfunc.sqlExeRet(statem)
		for column in domainsSqlOut:
			# Build the needed info 
			cDomainName = column[0] 
			cDomainId = int(column[1])
			# Append to results a creation of the rulesDomains object 
			self.RulesDomains.append(models.RulesDomain(cDomainName, cDomainId, InScopeObject.InScopeId, InScopeObject.ProgramId))

	

