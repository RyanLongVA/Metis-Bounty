#!/usr/bin/python
# Filename: mysqlfunc.py
# Purpose: All the mysql functions 


# !!! need to encapsulate a cur with something like a using statement

# Database errors
import MySQLdb, pdb, logger, dnsCheck
from MySQLdb import Error
#All the variables for paths
from variables import *

def create_dbConnection():
    try:
        # trying to create a connection with the proceeding connection
        a = MySQLdb.connect(user=databaseUser, passwd=databasePasswd, db=databaseName, unix_socket="/opt/lampp/var/mysql/mysql.sock")
        return a
    except Error as e:
        print(e)
    return None

def sqlExeCommit(statem):
    conn = create_dbConnection()
    cur = conn.cursor()
    cur.execute(statem)
    conn.commit()

def sqlCommit(conn):
    conn.commit()

# Only execute 
def sqlExe(cur, statem):

    cur.execute(statem)

# Execute return 
def sqlExeRet(statem):
    conn = create_dbConnection()
    cur = conn.cursor()
    cur.execute(statem)
    return cur.fetchall()

def sqlExeRetOne(statem):
    conn = create_dbConnection()
    cur = conn.cursor()
    cur.execute(statem)
    return cur.fetchone()

# Returns the domains based on the domainRangeId
def domainsBydomainRangeId(id):
    conn = create_dbConnection()
    cur = conn.cursor()
    statem = "SELECT domainName FROM Domains WHERE domainRangeId = %s"%str(id)
    cur.execute(statem)
    results = []
    for column in cur.fetchall():
        results.append(column[0])
    return results

# Returns the domains based on the domainRangeId
def domainIdsBydomainRangeId(id):
    conn = create_dbConnection()
    cur = conn.cursor()
    statem = "SELECT domainId FROM Domains WHERE domainRangeId = %s"%str(id)
    cur.execute(statem)
    results = []
    for column in cur.fetchall():
        results.append(int(column[0]))
    return results

# Returns the domains based on the domainRangeId
def domainNameByDomainId(id):
    conn = create_dbConnection()
    cur = conn.cursor()
    statem = "SELECT domainName FROM Domains WHERE domainId = %s"%str(id)
    cur.execute(statem)
    return cur.fetchone()[0]

# Return the domainRange value associated with the rangeId
def domainRangeByrangeId(cur, id):
    statem = "SELECT domainRange FROM InScope WHERE domainRangeId = %s"%str(id)
    cur.execute(statem)
    return cur.fetchone()[0]

# Return all scope Ids
def AllScopeIds(self):
        conn = mysqlfunc.create_dbConnection()
        cur = conn.cursor()
        # Saving the programI
        ScopeIds = []
        # Grab all the InScopeIds based on the programName
        statem = "SELECT domainRangeId FROM InScope"
        cur.execute(statem)
        for column in cur.fetchall():
            ScopeIds.append(int(column[0]))
        return ScopeIds

#Good for iterates on own commit
def insertDomain(domain, domainRangeId):
    conn = create_dbConnection()
    cur = conn.cursor()
    # checkInternet
    if dnsCheck.checkHostByName(domain):
        # pdb catch in case something goes wrong  
        # Find ips
        try: 
            # Insert into Domains 
            statem = "INSERT IGNORE INTO Domains(domainRangeId, domainName, dateFound) VALUES (%s, \"%s\", CURDATE())"%(domainRangeId, domain)
            cur.execute(statem)
            print '[+] New Domain:',domain
            logger.logNewDomain(domain)
        except Exception,e:
            print e 
            pdb.set_trace()
        # Commit 
        conn.commit()

def removeDomain(domain):
    conn = create_dbConnection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Domains WHERE domainName like \'%s\''%(domain))
    conn.commit()

def removeDomainArray(domainArray):
    conn = create_dbConnection()
    cur = conn.cursor()
    for domain in domainArray:
        cur.execute('DELETE FROM Ips WHERE domainId = (SELECT domainId FROM Domains where domainName = \'%s\')'%(domain))
        cur.execute('DELETE FROM Domains WHERE domainName like \'%s\''%(domain))
    conn.commit()

def returnAllDomains(cur):
    statem = "SELECT domainName FROM Domains"
    cur.execute(statem)
    results = [] 
    for column in cur.fetchall():
        results.append(column[0])
    return results


# Returns an Array of inScope Ids based onthe program
# oldName: returnInScopeIds
def InScopeIdsByProgramName(program):
    conn = create_dbConnection()
    cur = conn.cursor()
    statem = "SELECT domainRangeId FROM InScope WHERE programId = (SELECT programId FROM Programs WHERE name = \"%s\")"%(program)
    results = []
    cur.execute(statem)
    for a in cur.fetchall():
        results.append(int(a[0]))
    return results

def programNameByProgramId(programId):
    conn = create_dbConnection()
    cur = conn.cursor()
    statem = "SELECT name from Programs WHERE programId = %s"%programId
    cur.execute(statem)
    return cur.fetchone()[0]

def ProgramIdByProgramName(programName):
    conn = create_dbConnection()
    cur = conn.cursor()
    statem = "SELECT programId from Programs WHERE Programs = %s"%programId
    cur.execute(statem)
    return cur.fetchone()[0]

def blacklistedByDomainRangeId(cur, id):
    statem = "SELECT blacklistedContent FROM BlacklistedDomains WHERE domainRangeId = %s"%str(id)
    cur.execute(statem)
    results = []
    for a in cur.fetchall():
        results.append(a[0])
    return results