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
		for a in TaskListString.split(', '):
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
	def __init__(self, initScopeInput):
		self.RulesDomains = []
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
			try:  
				curProgramResults = getattr(ProgramRules, curRulesDomain.ProgramName)(curRulesDomain)
			except Exception,e:
				print '[!] Warning: Program {%s} Does not have a ProgramRulesEngine'
				curProgramResults = getattr(ProgramRules, curRulesDomain.ProgramName, default)
			pdb.set_trace()
			

			


	def rulesDomainsByInScopeId(self, InScopeObject):
		# create the connection and return all the domains 
		statem = "SELECT domainName, domainId FROM Domains WHERE domainRangeId = %s"%(InScopeObject.InScopeId)
		domainsSqlOut = mysqlfunc.sqlExeRet(statem)
		for column in domainsSqlOut:
			# Build the needed info 
			cDomainName = column[0] 
			cDomainId = int(column[1])
			# Append to results a creation of the rulesDomains object 
			self.RulesDomains.append(models.RulesDomain(cDomainName, cDomainId, InScopeObject.InScopeId, InScopeObject.ProgramId))

	

