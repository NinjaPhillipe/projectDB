import sqlite3
from operation import *

# db = sqlite3.connect("my_db.db")

dbSchema = DbSchema()
dbSchema.setDataBase("my_db.db")

# print(dbSchema.getDbschema())

req= Proj(['name'],Select(Eq('id',Cst(1)),Rel('users')))

# print(req.validation(dbSchema))
# print(req.toSql())
# print(req.sorte())
dbSchema.execute( Proj(['name',"age"],Select(Eq('id',Cst(1)),Rel('users'))))
