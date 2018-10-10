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
			resHttps = requests.get('https://'+curDomainRules.DomainName, verify=False, timeout=2)
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
		Global.__Response200__(self, resHttp=resHttp, resHttps=resHttps)
		Global.__Content0__(self, resHttp=resHttp, resHttps=resHttps)

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
							parsingSqlData.InsertDomainWrapper(newDomains, curInScope.InScopeId)
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
							parsingSqlData.InsertDomainWrapper(newDomains, curInScope.InScopeId)
						self.Score += -75
						self.Results.append('Redirection_Https_Meta')
					else:
						# This http-equiv refresh tag is mostly not a redirect
						print "Odd meta http-equiv refresh tag from: "+resHttps.url+" \t Tag: "+result
						logger.logInteresting("Odd meta http-equiv refresh tag from: "+resHttps.url+" \t Tag: "+result)

	def __ResponseExistence__(self, resHttp, resHttps):
		if resHttp == None: 
			self.Score += -50
			self.Results.append('ResponseExistence_Http')
		if resHttps == None:
			self.Score += -75
			self.Results.append('ResponseExistence_Https')

	def __Response200__(self, resHttp = None, resHttps = None):
		try:
			if resHttp.status_code == 200:
				self.Score += 30
				self.Results.append('Response200_Http')
		except:
			pass
		try:
			if resHttps.status_code == 200:
				self.Score += 30
				self.Results.append('Response200_Https')
		except:
			pass
	def __Content0__(self, resHttp = None, resHttps = None):
		try: 
			if len(resHttps.content) == 0:
				self.Score += -50
				self.Results.append('Content0_Https')
		except:
			pass
		try:
			if len(resHttp.content) == 0:
				self.Score += -50
				self.Results.append('Content0_Http')
		except:
			pass


		

		