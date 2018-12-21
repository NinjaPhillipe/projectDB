import sqlite3
from SqlFromSPJRUD import *

# db = sqlite3.connect("my_db.db")

dbSchema = DbSchema()
dbSchema.setDataBase("my_db.db")
# select * from job union select id,job_name,sal from (job_hiver);

print(dbSchema.getDbschema())

# print(req.validation(dbSchema))
# print(req.toSql())
# print(req.sorte())
# dbSchema.execute( Union(Rel("job"),Rel("job_hiver")) ) # a mettre dans test unitaire
# dbSchema.execute( Diff(Rel("job"),Rel("job_hiver")) )
exp=Join( Union(Rel("job"),Rel("job_hiver")), Rel("annuaire"))
exp.validation(dbSchema)
print(exp.toSql())
dbSchema.execute(exp)
# dbSchema.createTable("test",Diff(Rel("job"),Rel("job_hiver")))

tt=Rename("id","test",Select(Eq("id",Cst(1)),Rel("users")))
print(tt.getSPJRUD())
print(exp.getSPJRUD())

exp=Select(Eq('firstname',Cst('Jean')),Rel('users'))
dbSchema.execute(exp)
exp = Select(Eq('firstname',Cst('Jean')),Rel('users')) + Select(Eq('firstname',Cst('Pierre')),Rel('users'))

dbSchema.execute(exp,True)

dbSchema.execute(Diff(Rel("annuaire"),Rel("users")))
