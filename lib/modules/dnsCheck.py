import socket, pdb

# Returns boolean if the domainName resolved or not
# (You should check the internet connection before calling this)
# Check cases:
# Cname/A/AAAA
def checkHostByName(domainName):
	try:
		result = socket.gethostbyname(domainName)
		if '192.168.0.1' in result:
			print '[-] '+domainName+' : '+result
			print '[*] Seems like it may have failed locally'
		else:
			return True
	except:
		return False

def checkInternet():
	try: 
		socket.gethostbyname('google.com')
		return True
	except:
		print '[-] Internet connect failed'
		return False