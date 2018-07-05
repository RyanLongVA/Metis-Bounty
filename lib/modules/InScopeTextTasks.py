import models, pdb, MySQLdb, logger, subprocess, parsingSqlData, os, sys, dnsCheck
import lib.modules.variables as variables
import mysqlfunc

## Tasks based on InScopes	

def Subfinder(InScopeObject):
	# Remove the wildcard
	print '[+] Starting Subfinder on: '+InScopeObject.ScopeText
	# Takes -d for domain && -o for name of the output file
	outputFileLoc = variables.tempFolder+'subfinder.temp'
	# Remove the files between 
	subprocess.call('rm '+outputFileLoc, shell=True)
	subprocess.call(variables.goBin+'subfinder -d %s -o %s'%(InScopeObject.ScopeText[2:], outputFileLoc), shell=True)
	try: 
		domainsOutput = subprocess.check_output('cat '+outputFileLoc, shell=True)
		newDomains = parsingSqlData.returnNewDomainsArrayInScopeObject(domainsOutput, InScopeObject)
		# Check Internet
		if dnsCheck.checkInternet():
			for domain in newDomains:
				mysqlfunc.insertDomain(domain, InScopeObject.InScopeId)
		else: 
			print '[-] Internet Check failed'
			logger.logError('[-] Internet check failed: '+', '.join(newDomains))
	
	except OSError,e:
		if e[0] == 2:
			print '[-] Subfinder errored out: By the fact that the output file does not exist\n'
			pdb.set_trace()
		else: 
			print '[-] Subfinder errored out: Weird error... debug in InScopeTextTasks >> subfinder function'
			pdb.set_trace()




# Need to add it to tasks dict
def Amass(InScopeObject):
	print '[+] Starting Amass on: '+InScopeObject.ScopeText
	# Takes -d for domain && -o for name of the output file
	outputFileLoc = variables.tempFolder+'amass.temp'
	# Remove the files between 
	subprocess.call('rm '+outputFileLoc, shell=True)
	subprocess.call(variables.goBin+'amass -d %s -o %s '%(InScopeObject.ScopeText[2:], outputFileLoc), shell=True)	
	try: 
		domainsOutput = subprocess.check_output('cat '+outputFileLoc, shell=True)
		newDomains = parsingSqlData.returnNewDomainsArrayInScopeObject(domainsOutput, InScopeObject)
		for domain in newDomains:
			mysqlfunc.insertDomain(domain, InScopeObject.InScopeId)
	
	except OSError,e:
		if e[0] == 2:
			print '[-] Amass errored out: By the fact that the output file does not exist\n'
			pdb.set_trace()
		else: 
			print '[-] Amass errored out: Weird error... debug in InScopeTextTasks >> subfinder function'
			pdb.set_trace()	

def Crtsh(InScopeObject):
	# Get all the domains based on the domainRangeId
	domainsList = mysqlfunc.domainsBydomainRangeId(InScopeObject.InScopeId)
	outputFileLoc = variables.tempFolder+'crtsh.temp'
	pdb.set_trace()	
	for domain in domainsList:
		# Clean
		subprocess.call('rm '+outputFileLoc, shell=True)
		# Call
		subprocess.call(variables.crtshPath+'/crt.sh %s %s'%(domain, outputFileLoc), shell=True)
		# Read 
		results = subprocess.check_output('cat '+outputFileLoc, shell=True)
		# Process
		pdb.set_trace()


def Gobuster(InScopeObject):
	# Output File Location 
	outputFileLoc = variables.tempFolder+'gobuster.temp'

	wordlistsPaths = os.listdir(variables.wordlistsDns)
	print '[+] Starting Gobuster on: '+InScopeObject.ScopeText
	print '[*] With Files: '+', '.join(wordlistsPaths)

	# Executing for every wordlist in wordlists/dns
	for fileName in wordlistsPaths:
		print '[+] Using file: '+fileName
		realPath = os.path.join(sys.path[0], variables.wordlistsDns, fileName)
		# Remove old output
		subprocess.call('rm '+outputFileLoc, shell=True)
		# The call
		print ''
		subprocess.call("gobuster -fw -m dns -u "+InScopeObject.ScopeText[2:]+" -t 100 -v -w "+realPath+" | tee "+outputFileLoc, shell=True)
		try: 
			# Parse output with sed and return the domains seperated by new line 
			domainsOutput = subprocess.check_output('cat '+outputFileLoc+" | sed -n -e s/'^Found: //p'", shell=True)
			newDomains = parsingSqlData.returnNewDomainsArrayInScopeObject(domainsOutput, InScopeObject)
			# Check the internet
			if dnsCheck.checkInternet():
				for domain in newDomains:
					mysqlfunc.insertDomain(domain, InScopeObject.InScopeId)
		
		except OSError,e:
			if e[0] == 2:
				print '[-] Gobuster errored out: By the fact that the output file does not exist\n'
				pdb.set_trace()
			else: 
				print '[-] Gobuster errored out: Weird error... debug in InScopeTextTasks >> subfinder function'
				pdb.set_trace()	
