#!/usr/bin/python
# Filename: mysqlfunc.py
# Purpose: All the mysql functions 


# !!! need to encapsulate a cur with something like a using statement

# Database errors
import MySQLdb, pdb
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

def sqlExeCommit(conn, statem):
    cur = conn.cursor()
    cur.execute(statem)
    conn.commit()

def sqlCommit(conn):
    conn.commit()

# Only execute 
def sqlExe(cur, statem):
    cur.execute(statem)


# Return the domainRange value associated with the rangeId
def domainRangeByrangeId(cur, id):
    
    statem = "SELECT domainRange FROM InScope WHERE domainRangeId = %s"%str(id)
    cur.execute(statem)
    return cur.fetchone()[0]

#Good for iterates on own commit
def insertDomain(cur, domain, domainRangeId, title=None):
    if title:
        #Insert with title
        #pdb catch in case something goes wrong 
        try:
            statem = "INSERT IGNORE INTO Domains(domainRangeId, domainName, domainTitle, dateFound) VALUES (%s, \"%s\", \"%s\", CURDATE())"%(domainRangeId, domain, title)
            cur.execute(statem)
        except Exception,e:
            print e 
            pdb.set_trace()
    else:
        #pdb catch in case something goes wrong  
        try: 
            statem ="INSERT IGNORE INTO Domains(domainRangeId, domainName, dateFound) VALUES (%s, \"%s\", CURDATE())"%(domainRangeId, domain)
            cur.execute(statem)
        except Exception,e:
            print e 
            pdb.set_trace()

def returnInScopeIds(cur, program):
    statem = "SELECT domainRangeId FROM InScope WHERE programId = (SELECT programId FROM Programs WHERE name = \"%s\")"%(program)
    print statem
    results = []
    cur.execute(statem)
    for a in cur.fetchall():
        results.append(int(a[0]))
    return results

def programNameToInScopeIds(conn, cProgram):
    # Returns the domainRangeId's for a program
    cur = conn.cursor()
    statem = "SELECT `domainRangeId` FROM InScope WHERE programId = (SELECT programId FROM Programs WHERE name = \'%s\')"%(cProgram)
    cur.execute(statem)
    b = [] 
    for a in cur.fetchall():
        b.append(int(a[0]))
    return b

def blacklistedByDomainRangeId(cur, id):
    statem = "SELECT blacklistedContent FROM BlacklistedDomains WHERE domainRangeId = %s"%str(id)
    cur.execute(statem)
    results = []
    for a in cur.fetchall():
        results.append(a[0])
    return results