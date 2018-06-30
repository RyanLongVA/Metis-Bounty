import pdb, MySQLdb, mysqlfunc
from MySQLdb import Error 
###Summary:
###General Paring before a insert


def filterBlacklistedFromDomainList(domainArray, outScope):
    try:
    	pdb.set_trace()
        #Domainlist >> brutesubs session
        domainArray = filter(None, domainArray)
    except:
        pass
    if domainArray == None:
        #Empty domain list
        a = []
    else:
        a = domainArray
    #a is the domainlist
    for b in outScope:
        #Check outScope value

        ###a will be only inscope
        if (b[:2] == '*.'):
            b = b[2:]
            for integer, c in reversed(list(enumerate(a))):
                # pdb.set_trace() 
                if c.find(c) != -1:
                    a.pop(integer)
        else:
            for integer, c in reversed(list(enumerate(a))):
                if c == b:
                    a.pop(integer)
    #List of inScope domains that were found
    #a is now a list of found InScope domains
    pdb.set_trace()
    return a

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

    # Remove duplicates from the b  
    for a in filter(None, domainArray.split('\n')):
        if a not in currentDomains and not a.startswith('.'):
            # It's definitely a unique domain
            currentUniques.append(a)

    # Make sure they are all inScope        
    if InScopeObject.ScopeText.startswith("*."):
        for domain in currentUniques:
            # check if inscope
            if domain.endswith(InScopeObject.ScopeText[2:]):
                continue
            else:
                print '\n\n[-] Domain:' + domain
                print 'Was not in: ' + InScopeObject.ScopeText 
                pdb.set_trace()
    else: 
        print '[-] Scope did not start with *.'
        print InScopeObject.ScopeText
        pdb.set_trace()
    return currentUniques


