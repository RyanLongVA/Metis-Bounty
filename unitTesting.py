import pdb

# lib/runners/inScope
import lib.modules.models as models

def libModels():
	## Check InScopeId
	a = models.InScope(1)	
	assert(a.ScopeText == '*.yahoo.com')
	b = models.InScope('*.yahoo.com')



def main():
	libModels()

main()