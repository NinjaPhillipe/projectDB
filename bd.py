import sqlite3
from operation import *

# db = sqlite3.connect("my_db.db")

dbSchema = DbSchema()
dbSchema.setDataBase("my_db.db")
# select * from job union select id,job_name,sal from (job_hiver);

print(dbSchema.getDbschema())

# print(req.validation(dbSchema))
# print(req.toSql())
# print(req.sorte())
# dbSchema.execute( Union(Rel("job"),Rel("job_hiver")) ) # a mettre dans test unitaire
dbSchema.execute(Diff(Rel("job"),Rel("job_hiver")) )
