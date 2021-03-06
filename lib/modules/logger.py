#Logging functions
import os

logFile = 'log.txt'
errorLogFile = 'errorLog.txt'
interestingLogFile = 'interestingLog.txt'

def logNewDomain(domainName):
	# Trim if too long
	if os.path.getsize(logFile) < 5000:
		f=open(logFile, 'a+')
		f.write('New Domain: '+ domainName+'\n')
		f.close()
	else:
		# Remove a specific amount of lines 
		f = open(logFile)
		count = 0
		output = []
		for line in f:
			if count < 20: 
				count += 1
				continue
			else:	
				output.append(line)	
		f.close()
		#Write the remaining
		f = open(logFile, 'w')
		f.writelines(output)
		f.close()

def logError(text):
	if os.path.getsize(errorLogFile) < 20000:
		f=open(errorLogFile, 'a+')
		f.write(text+'\n')
		f.close()
	else:
		# Remove a specific amount of lines 
		f = open(errorLogFile)
		count = 0
		output = []
		for line in f:
			if count < 20: 
				count += 1
				continue
			else:	
				output.append(line)	
		f.close()
		#Write the remaining
		f = open(errorLogFile, 'w')
		f.writelines(output)
		f.close()

def logInteresting(text):
		f=open(interestingLogFile, 'a+')
		f.write(text+'\n')
		f.close()