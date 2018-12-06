import sqlite3
from operation import *

#############################get col name#################
db = sqlite3.connect("my_db.db")
db.row_factory = sqlite3.Row
cursor = db.execute('select * from users')
# instead of cursor.description:
row = cursor.fetchone()
names = row.keys()
print(names)
##########################################################

# ("users",['id','name','age'],['INTEGER','TEXT','INTEGER'])

# dbschema = DBSchema()
# dbschema.add_table("Countries",["Name","Capital","Population"],["TEXT","TEXT","INTERGER"])

# db.connect("PATH")
# dbschema = DBSchema(db)

tab = Table("users",['id','name','age'],['INTEGER','TEXT','INTEGER'])

exp = Select(Eq("Population",Cst(100)),Rel("Countries"))
# exp=Select("tt",Rel("Countries"))

print(exp.valid)
if(exp.valid == True):
    print(exp.execute(db))
