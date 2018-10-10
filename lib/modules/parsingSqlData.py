import pdb, MySQLdb, mysqlfunc, logger, models, dnsCheck
from MySQLdb import Error 

###Summary:
###General Parsing 

def returnDomainsByRangeId(conn, domainId):
	#return all domains the current domain Id
	try:
		cur = conn.cursor()
		statem = "SELECT domainName FROM Domains WHERE domainRangeId = "+str(domainId)
		cur.execute(statem) 
		domainsWithinId = []
		results = []
		for a in cur.fetchall():
			domainsWithinId.append(a[0])
		return results
	except Exception,e:
		print '\n\n[-] removeDuplicatesByDomainId: exception statement pdb'
		print e
		pdb.set_trace()

def returnNewDomainsArrayInScopeObject(domainArray, InScopeObject):
    currentUniques = []
    conn = mysqlfunc.create_dbConnection()
    cur = conn.cursor()
    # Return the current domains of the scope
    currentDomains = []
    cur.execute("SELECT domainName from Domains WHERE domainRangeId = %s"%InScopeObject.InScopeId)
    for a in cur.fetchall():
        currentDomains.append(a[0])

    # Remove duplicates from domainArray 
    for a in domainArray:
        if a not in currentDomains and not a.startswith('.'):
            # It's definitely a unique domain
            currentUniques.append(a)
    # Make sure they are all inScope        
    if InScopeObject.ScopeText.startswith("*."):
        trueUniques = [x for x in currentUniques if x.endswith(InScopeObject.ScopeText[2:])]
    else: 
        trueUniques = []
        print '\t[-] Scope did not start with *.'
        print InScopeObject.ScopeText
    return trueUniques

def InsertDomainWrapper(domainArray, InScopeId):
    curInScope = models.InScope(InScopeId)
    newDomains = returnNewDomainsArrayInScopeObject(domainArray, curInScope)
    # Check Internet
    if dnsCheck.checkInternet():
        for domain in newDomains:
            mysqlfunc.insertDomain(domain, InScopeId)
    else: 
        print '[-] Internet Check failed'
        logger.logError('[-] Internet check failed: '+', '.join(newDomains))

