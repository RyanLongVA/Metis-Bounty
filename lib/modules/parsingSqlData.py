import pdb, MySQLdb 
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



