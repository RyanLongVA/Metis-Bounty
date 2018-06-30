import pdb
# The data models
import models
# The Tasks >> Consists of their runners 
import InScopeTextTasks as InScopeTextTasks

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
	def Tick(self):
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