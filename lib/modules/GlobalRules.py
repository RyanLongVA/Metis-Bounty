import pdb, requests
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
		pdb.set_trace()

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
		pdb.set_trace()
		Global.__RedirectionByStatusCode__(self, curDomainRules, resHttps, resHttp)		

	def __RedirectionByStatusCode__(self, curDomainRules, resHttps, resHttp):
		# Check https redirection
		if len(resHttps.history) != 0:
			# Grab all redirection urls and see if they are inScope
			redirectionArray
			for historyItem in resHttps.history:


		

		