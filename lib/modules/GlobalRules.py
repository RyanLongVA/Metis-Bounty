import pdb, requests, models, mysqlfunc, dnsCheck, logger, parsingSqlData
# Import urlparsing
from urlparse import urlparse


class Global:
	def __init__(self, curDomainRules):
		self.Results = []
		self.Score = 0
		for a in Global.__dict__.keys():
			if a.startswith('__'):
				continue
			else:
				getattr(Global, a)(self, curDomainRules)

	def RequestsReponseWrap(self, curDomainRules):
		# Https
		try:
			resHttps = requests.get('https://'+curDomainRules.DomainName)
			
		except Exception,e:
			resHttps = None # Most likely Connection/Error
			pass
		# Http
		try: 
			resHttp = requests.get('http://'+curDomainRules.DomainName)
		except Exception,e:
			resHttp = None
		Global.__RedirectionByStatusCode__(self, curDomainRules, resHttps, resHttp)
		Global.__ResponseExistence__(self, resHttp, resHttps)	

	def __RedirectionByStatusCode__(self, curDomainRules, resHttps, resHttp):
		# Check https redirection
		try:
			# If it redirected
			if len(resHttps.history) != 0:
				# Grab all redirection urls and see if they are inScope
				redirectionArray = []
				for historyItem in resHttps.history:
					redirectionArray.append(urlparse(historyItem.url).netloc)
				# Have to initialize a InScope class to send to the next function
				curInScope = models.InScope(curDomainRules.InScopeId)
				newDomains = parsingSqlData.returnNewDomainsArrayInScopeObject(redirectionArray, curInScope)
				if len(newDomains) != 0:
					print '[+] New Domains from redirect'
					print '[*] Origin:',curDomainRules.DomainName
					print '[*] Array:',', '.join(newDomains)
					parsingSqlData.InsertDomainWrapper(newDomains, curInScope.InScopeId)

				# Checking to see if http exists
				if resHttp == None:
					# Adding score if there was no Http response
					self.Score += -100
					self.Results.append('RedirectionByStatusCode')
				else:
					# Don't need to try/except >> if resHttp is not None, than it's a response object with a history attribute 
					if len(resHttp.history) != 0:
						# Else http doesn't redirect and https does
						# Parse http

						redirectionArray = [] 
						for historyItem in resHttp.history:
							redirectionArray.append(urlparse(historyItem.url).netloc)
						curInScope = models.InScope(curDomainRules.InScopeId)
						newDomains = parsingSqlData.returnNewDomainsArrayInScopeObject(redirectionArray, curInScope)
						if len(newDomains) != 0:
							print '[+] New Domains from redirect'
							print '[*] Origin:',curDomainRules.DomainName
							print '[*] Array:',', '.join(newDomains)
							parsingSqlData.InsertDomainWrapper(newDomains, curInScope.InScopeId)
						self.Score += -100
						self.Results.append('RedirectionByStatusCode')

		except AttributeError,e:
			# Check if it's from the history key
			if 'history' in e[0]:
				# Https response was None
				try:
					if len(resHttp.history) != 0:
						redirectionArray = []
						for historyItem in resHttp.history:
							redirectionArray.append(urlparse(historyItem.url).netloc)
						# Have to initialize a InScope class to send to the next function
						curInScope = models.InScope(curDomainRules.InScopeId)
						newDomains = parsingSqlData.returnNewDomainsArrayInScopeObject(redirectionArray, curInScope)
						if len(newDomains) != 0:
							print '[+] New Domains from redirect'
							print '[*] Origin:',curDomainRules.DomainName
							print '[*] Array:',', '.join(newDomains)
							parsingSqlData.InsertDomainWrapper(newDomains, curInScope.InScopeId)
						self.Score += -100
						self.Results.append('RedirectionByStatusCode')
				except:
					# Http Response was none
					pass
			else:
				print '[-] An unexpected error occured'
				print e
				pdb.set_trace()

	def __ResponseExistence__(self, resHttps, resHttp):
		if (resHttp == None) and (resHttps == None):
			self.Score += -200
			self.Results.append('ResponseExistence')




		

		