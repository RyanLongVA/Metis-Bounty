import pdb
# The data models
import models
# The Tasks >> Consists of their runners 
import InScopeTextTasks as InScopeTextTasks
# Import the handy database strings
import mysqlfunc
# Importing the Rules
import ProgramRules, GlobalRules
# Multithreading
from multiprocessing.dummy import Pool as ThreadPool

### Runners ###

class ReconManager:
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
					ReturningIds = mysqlfunc.InScopeIdsByAll()
				else:
					ReturningIds = mysqlfunc.InScopeIdsByProgramName(scope) 
				self.Queue = []
				for a in ReturningIds:
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
		self.RulesIps = []
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
				InScopeIds = mysqlfunc.InScopeIdsByProgramName(initScopeInput)
			else: 
				# We start based on the inScopeId
				InScopeIds.append(initScopeInput)
			# Use the InScopeId(s) to create the RulesDomain objects and append them to the list
			for curId in InScopeIds: 
				# Creation of the InScope
				curIdObject = models.InScope(curId)
				self.rulesDomainsByInScopeId(curIdObject)

	def Execute(self):
		# Pool and multithread
		pool = ThreadPool(75)
		pool.map(RulesEngineManager.RulesWrapping, self.RulesIps)
		#for a in self.RulesIps:
		#	RulesEngineManager.RulesWrapping(a)
	@staticmethod
	def RulesWrapping(rulesDomain):
		#try:
		print '[+] Starting on %s:%s'%(rulesDomain.DomainName,rulesDomain.IpAddress)
		# Run Globals
		curGlobalResults = GlobalRules.Global(rulesDomain)
		# Run Program depth rules
		if hasattr(ProgramRules, rulesDomain.ProgramName):
			curProgramResults = getattr(ProgramRules, rulesDomain.ProgramName)(rulesDomain)
		else:
			print '\t[!] Warning: Program {%s} Does not have a ProgramRulesEngine'
			# Set as BlankClass so stats don't break
			curProgramResults = getattr(ProgramRules, 'BlankClass')(rulesDomain)

		# Set vars: Combine score, Global.Results, Program.Results
		CombinedScore = curGlobalResults.Score + curProgramResults.Score
		# Update in database 
		print '\t RulesScore: %s'%CombinedScore
		print '\t Global: %s'%','.join(curGlobalResults.Results)
		print '\t Program: %s'%','.join(curProgramResults.Results)
		print ''
		statem = "UPDATE Ips SET RulesScore = %s, RulesGlobal = \'%s\', RulesProgram = \'%s\' WHERE domainId = %s"%(CombinedScore, ','.join(curGlobalResults.Results), ','.join(curProgramResults.Results), rulesDomain.DomainId)
		mysqlfunc.sqlExeCommit(statem)
		#except Exception,e:
		#	print "Error Caught @ runners.RulesEngineManager.RulesWrapping: "
		#	print e 
		#	pdb.set_trace()

	def rulesDomainByDomain(self, domain):
		if self.OnlyNotCalculated:
			statem = "SELECT a.domainName, a.domainId, a.domainRangeId, b.ipAddress, c.programId, d.name FROM Domains as a join Ips as b on a.domainId = b.domainId join InScope as c on a.domainRangeId = c.domainRangeId join Programs as d on c.programId = d.programId WHERE a.domainName = \'%s\' AND RulesScore IS NULL"%domain
		else:
			statem = "SELECT a.domainName, a.domainId, a.domainRangeId, b.ipAddress, c.programId, d.name FROM Domains as a join Ips as b on a.domainId = b.domainId join InScope as c on a.domainRangeId = c.domainRangeId join Programs as d on c.programId = d.programId WHERE a.domainName = \'%s\'"%domain
		result = mysqlfunc.sqlExeRet(statem)
		if len(result) < 1:
			print '  [-] No results'
			print '    [*] Info: '+statem
			exit()
		# Log Basics

		for column in result:
			self.RulesIps.append(models.RulesIp(column[0], column[1], column[2], column[3], column[4], column[5]))

	def rulesDomainsByInScopeId(self, InScopeObject):
		# create the connection and return all the domains 
		if self.OnlyNotCalculated:
			statem = "SELECT a.domainName, a.domainId, a.domainRangeId, b.ipAddress, c.programId, d.name FROM Domains as a join Ips as b on a.domainId = b.domainId join InScope as c on a.domainRangeId = c.domainRangeId join Programs as d on c.programId = d.programId WHERE a.domainRangeId = %s and RulesScore IS NULL"%(InScopeObject.InScopeId)
		else:	
			statem = "SELECT a.domainName, a.domainId, a.domainRangeId, b.ipAddress, c.programId, d.name FROM Domains as a join Ips as b on a.domainId = b.domainId join InScope as c on a.domainRangeId = c.domainRangeId join Programs as d on c.programId = d.programId WHERE a.domainRangeId = %s"%(InScopeObject.InScopeId)
		domainsSqlOut = mysqlfunc.sqlExeRet(statem)
		for column in domainsSqlOut:
			# Append to results a creation of the rulesDomains object 
			self.RulesIps.append(models.RulesIp(column[0], column[1], column[2], column[3], column[4], column[5]))

# Checking Ips
class DomainResolve:
	def __init__(self, program = None, ip = None, domainRangeId = None, domain = None):
		if program:
			# self.ipsObjects = []
			self.domainObjects = []

			# Return on Scope ids
			scopes = mysqlfunc.InScopeIdsByProgramName(program)
			if len(scopes) is 0:
				print '[-] No domainRangeIds in:', program
				print '[-] Exiting'
				exit()
			# Get all of the domains
			domainIds = [] 
			for a in scopes:
				domainIds += mysqlfunc.domainIdsBydomainRangeId(a)

			for a in domainIds:
				domainSqlData = mysqlfunc.sqlExeRetOne('SELECT domainId, domainName, domainRangeId from Domains where domainId = %s'%a)
				self.domainObjects.append(models.Domain(domainSqlData[0], domainSqlData[1], domainSqlData[2]))
			
			# Insert new Ips record 
			# 	INSERT into Ips (domainId, ipAddress, dateFound, dateChecked) VALUES ((select domainId from Domains where domainName = 'flicker.com'), '212.82.102.24', now(), now())
	def DomainsCheck(self, threads = 10):
		def domainsThreaded(a):
			a.GrabIps()
			# Check that they exist in sql
			print '[*]',a.DomainName,':',','.join(a.Ips)
			for b in a.Ips:
				if b is '0.0.0.0':
					continue
				if not mysqlfunc.sqlExeRetOne("select domainId from Ips where ipAddress = \'"+b+"\' and domainId = "+str(a.DomainId)):
					# The pair doesn't exist
					mysqlfunc.sqlExeCommit("INSERT into Ips (domainId, ipAddress, dateFound, dateChecked) VALUES ("+str(a.DomainId)+", \'"+b+"\', now(), now())")
		pool = ThreadPool(threads)
		pool.map(domainsThreaded, self.domainObjects)


class CheckDomainResolveFromIps:
	def __init__(self, program = None, ip = None, domainRangeId = None, domain = None):
		if program:
			# self.ipsObjects = []
			self.ipObjects = []

			# Return on Scope ids
			scopes = mysqlfunc.InScopeIdsByProgramName(program)
			if len(scopes) is 0:
				print '[-] No domainRangeIds in:', program
				print '[-] Exiting'
				exit()
			# Get all of the domains
			domainIds = [] 
			for a in scopes:
				domainIds += mysqlfunc.domainIdsBydomainRangeId(a)
			ipSql = mysqlfunc.sqlExeRet('SELECT distinct ipAddress from Ips where domainId IN ('+','.join(str(x) for x in domainIds)+')')
			for a in ipSql:
				self.ipObjects.append(models.Ip(a[0]))
	def Execute(self, threads = 10):
		def selfExe(myObject):
			myObject.ReverseResolve()
		for a in self.ipObjects:
			a.GrabDomains()
		# Breaking up the functions so there's no environment for race conditions
		pool = ThreadPool(threads)
		pool.map(selfExe, self.ipObjects)
		#for a in self.ipObjects:
		#	a.ReverseResolve()







					



