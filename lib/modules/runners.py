### Runners ###

import sys
import MySQLdb, pdb
from MySQLdb import Error
from .. import mysqlfunc
# All the variables for paths


class InScope:

	def __init__(self, InScopeId):
		# Create the database connection 
		conn = create_dbConnection()
		cur = conn.cursor()
		# Grab scope text by scope Id
		self.ScopeText = domainRangeByrangeId(cur, InScopeId)
		pdb.set_trace()
