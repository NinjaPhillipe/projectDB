import sqlite3
from operation import *

db = sqlite3.connect("my_db.db")

dbSchema = DbSchema("my_db.db")

print(dbSchema.getDbschema())

##############ERROR#########
req = Rel('CC')
print(req.execute(dbSchema))

###############WORK###########
req = Rel('users')
print(req.execute(dbSchema))
