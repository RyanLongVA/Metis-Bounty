import requests, pdb
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
#
class BlankClass:
	def __init__(self, curDomainRules):
		self.Results = []
		self.Score = 0

class Tesla:
	def __init__(self, curDomainRules):
		self.Results = []
		self.Score = 0
		for a in Telsa.__dict__.keys():
			if a.startswith('__'):
				continue 
			else:
				getattr(Tesla, a)(self, curDomainRules)


class Yahoo:
	def __init__(self, curDomainRules):
		self.Results = []
		self.Score = 0
		for a in Yahoo.__dict__.keys():
			if a.startswith('__'):
				continue 
			else:
				getattr(Yahoo, a)(self, curDomainRules)
	def RequestResponseWrap(self, curDomainRules):
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
		Yahoo.__Sorry_Page_Not_Found_Common__(self, resHttp, resHttps)
		Yahoo.__Site_Under_Construction_Common__(self, resHttp, resHttps)
		Yahoo.__Ad_Manager_Plus_Common__(self, resHttp, resHttps)
		Yahoo.__Need_Login_Yahoosmallbusiness__(self, resHttp, resHttps)
	def __Sorry_Page_Not_Found_Common__(self, resHttp, resHttps):
		# Based on example: https://av-beapa10.adx.vip.ir2.yahoo.com/
		if resHttp:
			if '<p>Please check the URL for proper spelling and capitalization. If you\'re having trouble locating a destination on Yahoo!, try visiting the <strong><a href="http://us.rd.yahoo.com/default/*http://www.yahoo.com">Yahoo! home page</a></strong> or look through a list of <strong>' in resHttp.content:
				self.Score += -75
				self.Results.append('Sorry_Page_Not_Found_Common_Http')
		if resHttps:
			if '<p>Please check the URL for proper spelling and capitalization. If you\'re having trouble locating a destination on Yahoo!, try visiting the <strong><a href="http://us.rd.yahoo.com/default/*http://www.yahoo.com">Yahoo! home page</a></strong> or look through a list of <strong>' in resHttps.content:
				self.Score += -75
				self.Results.append('Sorry_Page_Not_Found_Common_Https')

	def __Site_Under_Construction_Common__(self, resHttp, resHttps):
		if resHttp:
			if '<head> <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"> <meta name="robots" content="noindex,nofollow">  <title>This site is under construction.</title>  <link href="http://geocities.com/js_source/lander-1.css" rel="stylesheet" type="text/css"></head>' in resHttp.content:
				self.Score += -75
				self.Results.append('Site_Under_Construction_Common_Http')
		if resHttps:
			if '<head> <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"> <meta name="robots" content="noindex,nofollow">  <title>This site is under construction.</title>  <link href="http://geocities.com/js_source/lander-1.css" rel="stylesheet" type="text/css"></head><' in resHttps.content:
				self.Score += -75
				self.Results.append('Site_Under_Construction_Common_Https')
	def __Ad_Manager_Plus_Common__(self, resHttp, resHttps):
		if resHttp:
			if 'Welcome to Yahoo Ad Manager Plus (YAM+)!' == resHttp.content:
				self.Score += -80
				self.Results.append('Ad_Manager_Plus_Http')
		if resHttps:
			if 'Welcome to Yahoo Ad Manager Plus (YAM+)!' == resHttps.content:
				self.Score += -80
				self.Results.append('Ad_Manager_Plus_Http')
	def __Need_Login_Yahoosmallbusiness__(self, resHttp, resHttps):
		if resHttp:
			if resHttp.url.startswith('https://login.yahoosmallbusiness.com/login'):
				self.Score += -20
				self.Results.append('Need_Login_Yahoosmallbusiness__Http')
		if resHttps:
			if resHttps.url.startswith('https://login.yahoosmallbusiness.com/login'):
				self.Score += -20
				self.Results.append('Need_Login_Yahoosmallbusiness__Https')
	def __Not_Found_On_Accelerator__(self, resHttp, resHttps):
		if resHttp:
			if '<TITLE>Not Found on Accelerator</TITLE>' in resHttp:
				self.Score += -20
				self.Results.append('Not_Found_On_Accelerator__Http')
		if resHttps:
			if '<TITLE>Not Found on Accelerator</TITLE>' in resHttps:
				self.Score += -20
				self.Results.append('Not_Found_On_Accelerator__Https')
