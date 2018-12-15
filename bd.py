import sqlite3
from operation import *

# db = sqlite3.connect("my_db.db")

dbSchema = DbSchema()
dbSchema.setDataBase("my_db.db")

print(dbSchema.getDbschema())
