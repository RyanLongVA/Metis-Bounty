import pdb, requests, models, mysqlfunc, dnsCheck, logger, parsingSqlData, BeautifulSoup
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
			resHttps = requests.get('https://'+curDomainRules.DomainName, timeout=2)
		except Exception,e:
			resHttps = None # Most likely Connection/Error
			pass
		# Http
		try: 
			resHttp = requests.get('http://'+curDomainRules.DomainName, timeout=2)
		except Exception,e:
			resHttp = None
		Global.__Redirection__(self, curDomainRules, resHttp, resHttps)
		Global.__ResponseExistence__(self, resHttp, resHttps)


	# def __RedirectionByMetaTag__(self, curDomainRules, resHttps, resHttp):
	# 	# The idea is to check if all the available responses are cut by metadata
	# 	AllMetaRedirects = False
	# 	MetaRedirects = []
	# 	for a in filter(None, [resHttps, resHttp]):
	# 		soup = BeautifulSoup.BeautifulSoup(a.text)
	# 		result = soup.find("meta", attrs={"http-equiv":"refresh"})
	# 		print result
	# 		if result:
	# 			wait,text=result["content"].split(";")
	# 			if text.strip().lower().startswith("url="):
	# 				# it redirects
	# 				MetaRedirects.append(str(urlparse(text[4:]).netloc))
	# 				AllMetaRedirects = True
	# 			else:
	# 				# This http-equiv refresh tag is mostly not a redirect
	# 				print "Odd meta http-equiv refresh tag from: "+a.url+" \t Tag: "+result
	# 				logger.logInteresting("Odd meta http-equiv refresh tag from: "+a.url+" \t Tag: "+result)
	# 				AllMetaRedirects = False
	# 				break
	# 		else:
	# 			# No meta refresh
	# 			AllMetaRedirects = False
	# 			break
	# 	if len(MetaRedirects) != 0:
	# 		curInScope = models.InScope(curDomainRules.InScopeId)
	# 		parsingSqlData.InsertDomainWrapper(MetaRedirects, curInScope.InScopeId)

	# 	if AllMetaRedirects == False:
	# 		return
	# 	else: 
	# 		# Add to score and results
	# 		self.Score += -100
	# 		self.Results.append('RedirectionByMetaTag')
	

	def __Redirection__(self, curDomainRules, resHttp, resHttps):
		if resHttp:
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
				self.Score += -25
				self.Results.append('Redirection_StatusCode_Http')
			else: 
				# Check meta
				soup = BeautifulSoup.BeautifulSoup(resHttp.text)
				result = soup.find("meta", attrs={"http-equiv":"refresh"})
				if result:
					wait,text=result["content"].split(";")
					if text.strip().lower().startswith("url="):
						# it redirects
						MetaRedirect = str(urlparse(text[4:]).netloc)
						curInScope = models.InScope(curDomainRules.InScopeId)
						newDomains = parsingSqlData.returnNewDomainsArrayInScopeObject([MetaRedirect], curInScope)
						if newDomains != 0:
							print '[+] New Domains from redirect'
							print '[*] Origin:',curDomainRules.DomainName
							print '[*] Array:',', '.join(newDomains)
							parsingSqlData.InsertDomainWrapper(newDomains, curInscope.InScopeId)
						self.Score += -25
						self.Results.append('Redirection_Meta_Http')
					else:
						# This http-equiv refresh tag is mostly not a redirect
						print "Odd meta http-equiv refresh tag from: "+resHttp.url+" \t Tag: "+result
						logger.logInteresting("Odd meta http-equiv refresh tag from: "+resHttp.url+" \t Tag: "+result)
		if resHttps:
			if len(resHttps.history) != 0:
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
				self.Score += -75
				self.Results.append('Redirection_Https_StatusCode')
			else: 
				# Check meta
				soup = BeautifulSoup.BeautifulSoup(resHttps.text)
				result = soup.find("meta", attrs={"http-equiv":"refresh"})
				if result:
					wait,text=result["content"].split(";")
					if text.strip().lower().startswith("url="):
						# it redirects
						MetaRedirect = str(urlparse(text[4:]).netloc)
						curInScope = models.InScope(curDomainRules.InScopeId)
						newDomains = parsingSqlData.returnNewDomainsArrayInScopeObject([MetaRedirect], curInScope)
						if newDomains != 0:
							print '[+] New Domains from redirect'
							print '[*] Origin:',curDomainRules.DomainName
							print '[*] Array:',', '.join(newDomains)
							parsingSqlData.InsertDomainWrapper(newDomains, curInscope.InScopeId)
						self.Score += -75
						self.Results.append('Redirection_Https_Meta')
					else:
						# This http-equiv refresh tag is mostly not a redirect
						print "Odd meta http-equiv refresh tag from: "+resHttps.url+" \t Tag: "+result
						logger.logInteresting("Odd meta http-equiv refresh tag from: "+resHttps.url+" \t Tag: "+result)


	# def __RedirectionByStatusCode__(self, curDomainRules, resHttps, resHttp):
	# 	# Check https redirection
	# 	try:
	# 		# If it redirected
	# 		if len(resHttps.history) != 0:
	# 			# Grab all redirection urls and see if they are inScope
	# 			redirectionArray = []
	# 			for historyItem in resHttps.history:
	# 				redirectionArray.append(urlparse(historyItem.url).netloc)
	# 			# Have to initialize a InScope class to send to the next function
	# 			curInScope = models.InScope(curDomainRules.InScopeId)
	# 			newDomains = parsingSqlData.returnNewDomainsArrayInScopeObject(redirectionArray, curInScope)
	# 			if len(newDomains) != 0:
	# 				print '[+] New Domains from redirect'
	# 				print '[*] Origin:',curDomainRules.DomainName
	# 				print '[*] Array:',', '.join(newDomains)
	# 				parsingSqlData.InsertDomainWrapper(newDomains, curInScope.InScopeId)

	# 			# Checking to see if http exists
	# 			if resHttp == None:
	# 				# Adding score if there was no Http response
	# 				self.Score += -100
	# 				self.Results.append('RedirectionByStatusCode')
	# 			else:
	# 				# Don't need to try/except >> if resHttp is not None, than it's a response object with a history attribute 
	# 				if len(resHttp.history) != 0:
	# 					# Else http doesn't redirect and https does
	# 					# Parse http

	# 					redirectionArray = [] 
	# 					for historyItem in resHttp.history:
	# 						redirectionArray.append(urlparse(historyItem.url).netloc)
	# 					curInScope = models.InScope(curDomainRules.InScopeId)
	# 					newDomains = parsingSqlData.returnNewDomainsArrayInScopeObject(redirectionArray, curInScope)
	# 					if len(newDomains) != 0:
	# 						print '[+] New Domains from redirect'
	# 						print '[*] Origin:',curDomainRules.DomainName
	# 						print '[*] Array:',', '.join(newDomains)
	# 						parsingSqlData.InsertDomainWrapper(newDomains, curInScope.InScopeId)
	# 					self.Score += -100
	# 					self.Results.append('RedirectionByStatusCode')

	# 	except AttributeError,e:
	# 		# Check if it's from the history key
	# 		if 'history' in e[0]:
	# 			# Https response was None
	# 			try:
	# 				if len(resHttp.history) != 0:
	# 					redirectionArray = []
	# 					for historyItem in resHttp.history:
	# 						redirectionArray.append(urlparse(historyItem.url).netloc)
	# 					# Have to initialize a InScope class to send to the next function
	# 					curInScope = models.InScope(curDomainRules.InScopeId)
	# 					newDomains = parsingSqlData.returnNewDomainsArrayInScopeObject(redirectionArray, curInScope)
	# 					if len(newDomains) != 0:
	# 						print '[+] New Domains from redirect'
	# 						print '[*] Origin:',curDomainRules.DomainName
	# 						print '[*] Array:',', '.join(newDomains)
	# 						parsingSqlData.InsertDomainWrapper(newDomains, curInScope.InScopeId)
	# 					self.Score += -100
	# 					self.Results.append('RedirectionByStatusCode')
	# 			except:
	# 				# Http Response was none
	# 				pass
	# 		else:
	# 			print '[-] An unexpected error occured'
	# 			print e
	# 			pdb.set_trace()

	def __ResponseExistence__(self, resHttp, resHttps):
		if not resHttp: 
			self.Score += -50
			self.Results.append('ResponseExistence_Http')
		if not resHttps:
			self.Score += -75
			self.Results.append('ResponseExistence_Https')




		

		