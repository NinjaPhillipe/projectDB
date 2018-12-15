import unittest
from operation import *

dbSchema = DbSchema("my_db.db")

##############ERROR#########
rel = Rel('CC')
print("Expected ERROR :",rel.validation(dbSchema))

###############WORK###########
rel = Rel('users')
print("Expected WORK :",rel.validation(dbSchema))

############################SELECT###############################
select = Select(Eq("id",Cst(0)),Rel("users"))
print("Expected WORK :",select.validation(dbSchema))

select = Select(Eq("id",Cst(0)),Rel("us"))
print("Expected ERROR :",select.validation(dbSchema))

select = Select(Eq("id",Cst("0")),Rel("users"))
print("Expected ERROR :",select.validation(dbSchema))

select = Select(Eq("shitshit",Cst(0)),Rel("users"))
print("Expected ERROR :",select.validation(dbSchema))
# ##########################PROJECTION#############################
# print("\n PROJECTION")
# proj = Proj(["Country","Money"],select)
# print(proj.validation("TEST"))
#
# proj2 = Proj(["Country","Money"],rel)
# print(proj2.validation("TEST"))
#
# #ERROR
# proj3 = Proj(["Country","Money"],eq)
# print(proj3.validation("TEST"))
#
# #############################JOIN################################
# print("\n JOIN")
#
# ############################RENAME###############################
# print("\n RENAME")
# rename = Rename("Country","Land",rel)
# print(rename)
#
# ############################UNION################################
# print("\n UNION")
# union = Union(select,select)
# print(union.validation("TEST"))
# ##########################DIFFERENCE#############################
# print("\n DIFFERENCE")
# diff = Diff(select,select)
# print(diff.validation("TEST"))
# ############################Global###############################
# print("\n GLOBAL")

# glob = Proj(["Population"],Join(Rename("Name", "Capital", Rel("Cities")),Select(Eq("Country", Cst("Mali")),Rel("CC"))))
# print(glob)


class MyTest(unittest.TestCase):
    dbSchema = DbSchema("my_db.db")
    def test_Cst(self):
        self.assertEqual(Cst(0).type,"INTEGER")
        self.assertEqual(Cst("0").type,"TEXT")
        self.assertEqual(Cst("rrrr").type,"TEXT")
        self.assertEqual(Cst(1.5).type,"REAL")
    def test_Select(self):
        select = Select(Eq("id",Cst(0)),Rel("users"))
        select.validation(self.dbSchema)
        self.assertTrue(select.isValid())

        select = Select(Eq("id",Cst(0)),Rel("us"))
        select.validation(self.dbSchema)
        self.assertFalse(select.isValid())

        select = Select(Eq("id",Cst("0")),Rel("users"))
        select.validation(self.dbSchema)
        self.assertFalse(select.isValid())

        select = Select(Eq("shitshit",Cst(0)),Rel("users"))
        select.validation(self.dbSchema)
        self.assertFalse(select.isValid())
if __name__ == '__main__':
    unittest.main()
