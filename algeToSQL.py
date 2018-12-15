import unittest
from operation import *

dbSchema = DbSchema()
dbSchema.setDataBase("my_db.db")

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
    dbSchema = DbSchema()
    dbSchema.tab = [['users', ['id', 'name', 'age'], ['INTEGER', 'TEXT', 'INTERGER']], ['annuaire', ['id', 'name', 'email', 'tel'], ['INTEGER', 'TEXT', 'TEXT', 'TEXT']]]
    def test_Cst(self):
        self.assertEqual(Cst(0).type,"INTEGER")
        self.assertEqual(Cst("0").type,"TEXT")
        self.assertEqual(Cst("rrrr").type,"TEXT")
        self.assertEqual(Cst(1.5).type,"REAL")
    def test_Rel(self):
        self.assertFalse(Rel('CC').validation(self.dbSchema))
        self.assertTrue(Rel('users').validation(self.dbSchema))
    def test_Select(self):
        select = Select(Eq("id",Cst(0)),Rel("users"))
        self.assertTrue(select.validation(self.dbSchema))
        self.assertEqual(select._sorte,['id', 'name', 'age'])

        select = Select(Eq("id",Cst(0)),Rel("us"))
        self.assertFalse(select.validation(self.dbSchema))

        select = Select(Eq("id",Cst("0")),Rel("users"))
        self.assertFalse(select.validation(self.dbSchema))

        select = Select(Eq("shitshit",Cst(0)),Rel("users"))
        self.assertFalse(select.validation(self.dbSchema))
if __name__ == '__main__':
    unittest.main()
