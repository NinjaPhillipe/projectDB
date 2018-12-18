import sqlite3
from operation import *

# db = sqlite3.connect("my_db.db")

dbSchema = DbSchema()
dbSchema.setDataBase("my_db.db")

# print(dbSchema.getDbschema())

req=Select(Eq("age",Cst(25)),Rel("users")) ### ERROR
# req=Rel("users")
test=Cst(25)

print(req.validation(dbSchema))
print(req.toSql())

dbSchema.execute(req)
