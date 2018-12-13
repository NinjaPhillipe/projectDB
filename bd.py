import sqlite3
from operation import *

db = sqlite3.connect("my_db.db")

dbSchema = DbSchema("my_db.db")

print(dbSchema.getDbschema())
