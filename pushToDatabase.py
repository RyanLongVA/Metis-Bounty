from __future__ import division

# As of 4-3-2018 I'm removing certain packages to clean up code... they're included in the new modules to save space: MySQLdb

# Note: There are some statements that I ignored and kept in code // now they have to be included in that module

import os, sys, pdb, subprocess, re string, argparse, time, socket, dns.resolver
#Decorator for timing up functions
from lib.modules import timeout
#MySQL functions and database errors
import lib.modules.mysqlfunc as mysqlfunc
#All the variables for paths
from lib.modules.variables import *
#General import parsing before a insert 
import lib.modules.parsingSqlData as parsingSqlData
#The models for the data
import lib.modules.models as models
#The runners for the data
import lib.modules.runners as runners


###Defining paths ++ which I've typical not included the ending blackslash
scriptFolder = sys.path[0]
tempFolder = sys.path[0]+'/tempFiles'
changesTXTFolder = sys.path[0]+'/lib/data'

###changes.txt is going to be in sys.path[0]+'/lib/data'
###Brutesub start script (brutesubs.sh) needs to be manual changed

###is the end slash necessary? I'd prefer if it wasn't and catered to the same style as scriptPath

#sys.argv[1] == databaseName
#sys.argv[2] == table

@timeout.timeout(1000)
def nmapOnDomain(domain, ports):
    #nmap -sS -A example.com --> faster tcp with OS Grepping
    #nmap -sU example.com --> UDP ports
    FNULL = open(os.devnull, 'w')
    portDict = {"full" : "-p-", "fast" : "-F", "normal": "", "simple" : "-p80,8080,8880,2052,2082,2086,2095,443,2053,2083,2087,2096,8443"}
    #portDict['full']
    inputFile = tempFolder+'/nmap.out'
    print 'Starting Nmap on: \t',domain
    ##Try and Except to find where nmap is breaking out... need the function to really return {}
    try:
        startOutput = subprocess.call('nmap -sS -sV -oG %s %s %s'%(inputFile, portDict[ports], domain), shell=True, stdout=FNULL)
        nmapOut = subprocess.check_output(nmapFormatFolder+'/scanreport.sh -f %s'%(inputFile), shell=True)
        ports = []
        portsJSON = {}
        for index, a in enumerate(nmapOut.split('\n')):
            #If the line is empty continue
            if a == '':
                continue
            # Skip the first line "Host: {IP} {Resolved domain}"
            if index != 0:
                tempArray = filter(None, a.split('\t\t'))
                tempArray2 = []
                for b in tempArray:
                    if b == '\t':
                        next
                    else:
                        tempArray2.append(b)
                portData = tempArray2[0].split()
                portStatus = portData[1]
                #Check the status of the port
                if portStatus != 'open':
                    continue
                portNumber = portData[0]
                #Check if port number is int type 
                if not isinstance(int(portNumber), int):
                    continue
                #Port socket type and Fingerprint
                portType = portData[2]
                portFingerprint = ' - '.join(tempArray[1:]).strip('\t')
                #Moving the information to the JSON array
                portsJSON[portNumber] = [portType, portFingerprint]
        return portsJSON
    except Exception,e:
        if e.message == 'Timer expired':
            pass
        print 'Line 246:'
        print e
        pdb.set_trace()

            
def grabWebTitle(domain):    
    command = "curl %s -sL -m 5 | tac | tac | awk -vRS=\"</title>\" \'/<title>/{gsub(/.*<title>|"%(domain)+r'\n'+"+/,\"\");print;exit}\'"
    return subprocess.check_output(command, shell=True)

def grabWebDNS(domain):
    try: 
        cdns = []
        b = socket.gethostbyname_ex(domain)
        if (b[0] == domain):
            ###Should be the same... so pretty much a 'A Record'
            cdns.append(b[0])
            d = []
            for c in b[2]:
                d.append(c)
            cdns.append(' , '.join(d))
        else: 
            for c in b[1]:
                cdns.append(c)
            d = []
            cdns.append(b[0])
            for c in b[2]:
                d.append(c)
            cdns.append(' , '.join(d))
        ##Add to the beginning... the domain
        cdns.insert(0, domain)
        data = ' : '.join(cdns)
        return data 
    except Exception,e:
        if e[0] == -2:
            print 'Failed: '+domain
        else: 
            print e
            # pdb.set_trace()


def callVirtualHost(domain, dnsLine):
    ipString = dnsLine.split(':')
    ipList = []
    for a in ipString[-1].split(' , '):
        a = a.strip()
        ipList.append(a)
    for a in ipList:
        print a
    os.system("gnome-terminal --working-directory=%s"%(virtualHostDiscoveryFolder))
    print 'Basic usage: ruby scan.rb --ip={IP ADDRESS} --host={TLD} (--port={port} >> When it\' not 80)'

def callWhatWeb(domain, port):
    try:
        if port == '80':
            whatwebOut = subprocess.check_output(whatWebPath + '/whatweb --color=NEVER -v %s'%('http://'+domain), shell=True)
        elif port == '443':
            whatwebOut = subprocess.check_output(whatWebPath + '/whatweb --color=NEVER -v %s'%('http://'+domain), shell=True)
        else:
            return None
        foundStatus = False
        statuscode = ''
        foundSummary = False
        summary = ''
        foundHeaderBegin = False
        foundHeaders = []
        foundHeaderEnd = False
        for line in whatwebOut.split('\n'):
            #Need to go through line by line and see why the .startswith() are turning false
            if not foundStatus:
                if line.startswith('Status'):
                    statuscode = line.split(' : ')[1].replace("\"", "").replace("\'", "")
                    foundStatus = True
                    continue
                else: 
                    continue
            if not foundSummary:
                if line.startswith('Summary'):
                    summary = line.split(' : ')[1].replace("'", "").replace('\"', '')
                    foundSummary = True
                    continue
                else:
                    continue
            if not foundHeaderBegin:
                if line.startswith('HTTP Headers:'):
                    foundHeaderBegin = True
                    continue
                else:
                    continue
            if line == '\t':
                foundHeaderEnd = True
            if not foundHeaderEnd:
                line2 = line.replace("\"", '').replace("'", "")
                foundHeaders.append(line2)
        foundHeaders = filter(None, foundHeaders)
        foundHeaders2 = []
        for cheader in foundHeaders:
            foundHeaders2.append(cheader.strip())
        foundHeaders = filter(None, foundHeaders2)

        fullOutput = [statuscode, summary, foundHeaders]
        # pdb.set_trace()
        return fullOutput
        #Both timeouts and non-http ports will error out

        #Just needs to return the formatted output ["StatusCode", "Summary", "Headers"]
    except Exception,e:
        print e
        if 'bad URI' in str(e):
            pdb.set_trace()
        return None
    ##Should return None or ['statuscode', 'summary', 'headers']

def returningStatuscode(prompt, domainListLength):
    a = []
    if prompt == 'next' or prompt.rstrip() == 'n':
        a.append(0)
        a.append(0)
    elif prompt.startswith('nc '):
        try:
            ### The line below is so the status code gets appended only after the port is verified as a number
            port = int(prompt[3:])
            a.append(1)
            a.append(int(prompt[3:]))
        except Exception,e:
            a.append(-1)
            a.append(prompt)
            print e
            pass
    elif prompt == 'info':
        a.append(2)
        a.append(2)
    elif prompt == 'checkInt':
        a.append(3)
        a.append(3)
    elif prompt.startswith('go '):
        try: 
            ### Same concept as for startswith('nc ')
            value = int(prompt[3:])
            if value > domainListLength-1:
                raise ValueError('[-] The Value(%s) was bigger than the domain list(%s)'%(value, domainListLength-1))
            a.append(4)
            a.append(int(prompt[3:]))
        except Exception,e: 
            a.append(-1)
            a.append(prompt)
            print e 
            pass
    elif prompt == 'goohak':
        a.append(5)
        a.append(5)
    elif prompt == 'virtualHost':
        a.append(6)
        a.append(6)
    else: 
        a.append(-1)
        a.append(prompt)
    return a
    # Seems tables are automatically saved i.e. don't need to be .commit()'d 

def callGobuster(domain, wordlistPath):
    try:
        # test = "gobuster -fw -m dns -u "+domain+" -t 100 -w "+wordlistPath+" | sed -n -e 's/^Found: //p' > "+tempFolder+'/gobuster.temp'
        test = "gobuster -fw -m dns -u "+domain+" -t 100 -v -w "+wordlistPath+" | tee "+tempFolder+'/gobuster.temp'
        subprocess.call(test, shell=True)
        b = subprocess.check_output("cat "+tempFolder+"/gobuster.temp | sed -n -e 's/^Found: //p'" , shell=True)
        c = filter(None, b.split('\n'))
        #check what the out of c is... should be a array of new domains
        return c
    except Exception, e:
        print 'Something went wrong with Gobuster'
        pdb.set_trace()
        print e

def mainGobuster(program, filename, conn):
    inScope = selectInScope(conn, program)
    #Deleted outScope... it needs a domainRangeId to run
    #Try selectOutScope
    checkLiveWebApp(conn, program+'_liveWebApp')
    numberOfFoundDomains = 0
    changesDomains = returnChangesDomains()
    for a in inScope:
        cleanTempFolder()
        if (a[:2] == '*.'):
            a = a[2:]
            b = callGobuster(a, filename)
            tableName = program+'_liveWebApp'
            c = checkLiveWebApp_Domains(conn, tableName, b, outScope)
            with conn.cursor() as cur:
                cfile = open(changesTXTFolder+'/changes.txt', 'a')
                for d in c:
                    if d in changesDomains:
                        continue
                    cur = conn.cursor()
                    statem = "SELECT * FROM "+tableName+" WHERE Domain=\'"+d+"\'"
                    cur.execute(statem)
                    if cur.fetchone():
                        next
                    else:
                        if b not in changesDomains:
                            numberOfFoundDomains =+ 1
                            print "[+] New Domain Found :",d
                            key = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(5)])
                            cfile.write('bounties ; '+tableName+' ; '+'Domain^'+d+' , Research Only^False ; False ; '+key+'\n')
                cfile.close()
        else:
            try: 
                cur = conn.cursor()
                statem = "INSERT INTO "+program+"_liveWebApp(`Domain`, `Research Only`) VALUES ('"+a+"','False')"''
                cur.execute(statem)
            except Exception, e:
                if e[0] == 1062:
                    pass
                else:
                    print e
                    pdb.set_trace()
    print "Total found: "+str(numberOfFoundDomains)

def returnChangesDomains():
    cfile = open(changesTXTFolder+'/changes.txt', 'r') 
    content = cfile.read()
    domains = []
    if len(content) == 0:
        return domains  
    for line in filter(None, content.split('\n')):
        aline = line.split(' ; ')[2].split(' , ')
        for cdata in aline:
            cdata = cdata.split('^')
            if cdata[0] == 'Domain':
                domains.append(cdata[1])
    return domains


def main(): 
    parser = argparse.ArgumentParser(description='databaseActions')
    
    parser.add_argument('-cd', action='store_true', help='"Program" Checks and rechecks domains from the program for DNS Records and deletes those that have disappeared')
    parser.add_argument('-s', help='The scope of the current data')
    parser.add_argument('-t', help='Tasks seperated by comma "Brutesubs, Subfinder, Crtsh"')
    parser.add_argument('--asn', action='store_true', help='Use the Asns')
    args = parser.parse_args()
    conn = mysqlfunc.create_dbConnection()
    curTest = conn.cursor()

    if args.s and args.t and not args.asn:
        # full logger
        CurrentQueue = runners.Manager(args.s, models.ScopeTypes[2], args.t)
        CurrentQueue.Tick()

    if args.cd:
        conn = mysqlfunc.create_dbConnection()
        cur = conn.cursor()
        domainsList = filter(None, mysqlfunc.returnAllDomains(cur))        
        fails1 = []
        try:
            socket.gethostbyname('google.com')
        except:
            print 'Internet connect failed'
            exit()
        for domain in domainsList:
            try: 
                b = socket.gethostbyname(domain)
            except Exception,e:
                if e[0] == -2:
                    fails1.append(domain)
                    print '[-] Failed: '+domain
                    continue
                else: 
                    print e 
                    exit()
            if b == '192.168.0.1':
                print '[-] Failed (locally?): '+domain
                fails1.append(domain)
            else:
                pass
        c = int(str(len(fails1)) + '00')
        d = len(domainsList)
        e = c / d 
        f = 5
        if e > f:
            for a in fails1:
                print a
            print '\nPercentage: '+str(e)+'%'
            print 'Fails Length: '+str(c)
            print 'Total Length: '+str(d)
            print 'More than '+str(f)+' percent failed\n\nDo you wish to continue?'
            while True:
                g = raw_input('(seriouslyYes/no) ')
                if g == 'seriouslyYes':
                    break
                elif g == 'no':
                    exit()
                else: 
                    print "Input was not understood"
        mysqlfunc.removeDomainArray(fails1)  

main()
