import unittest
from operation import *

dbSchema = DbSchema()
dbSchema.setDataBase('my_db.db')

# ##########################PROJECTION#############################
# print('\n PROJECTION')
# proj = Proj(['Country','Money'],select)
# print(proj.validation('TEST'))
#
# proj2 = Proj(['Country','Money'],rel)
# print(proj2.validation('TEST'))
#
# #ERROR
# proj3 = Proj(['Country','Money'],eq)
# print(proj3.validation('TEST'))
#
# #############################JOIN################################
# print('\n JOIN')
#
# ############################RENAME###############################
# print('\n RENAME')
# rename = Rename('Country','Land',rel)
# print(rename)
#
# ############################UNION################################
# print('\n UNION')
# union = Union(select,select)
# print(union.validation('TEST'))
# ##########################DIFFERENCE#############################
# print('\n DIFFERENCE')
# diff = Diff(select,select)
# print(diff.validation('TEST'))
# ############################Global###############################
# print('\n GLOBAL')

# glob = Proj(['Population'],Join(Rename('Name', 'Capital', Rel('Cities')),Select(Eq('Country', Cst('Mali')),Rel('CC'))))
# print(glob)


class MyTest(unittest.TestCase):
    dbSchema = DbSchema()
    dbSchema.tab = [['users', ['id', 'name', 'age'], ['INTEGER', 'TEXT', 'INTERGER']], ['annuaire', ['id', 'name', 'email', 'tel'], ['INTEGER', 'TEXT', 'TEXT', 'TEXT']]]
    def test_Cst(self):
        self.assertEqual(Cst(0).getType(),'INTEGER')
        self.assertEqual(Cst('0').getType(),'TEXT')
        self.assertEqual(Cst('rrrr').getType(),'TEXT')
        self.assertEqual(Cst(1.5).getType(),'REAL')
    def test_Rel(self):
        self.assertFalse(Rel('CC').validation(self.dbSchema))
        self.assertTrue(Rel('users').validation(self.dbSchema))
        self.assertTrue(Rel('users').toRel().validation(self.dbSchema))
    def test_Select(self):
        #projection sur une colonne
        select = Select(Eq('id',Cst(0)),Rel('users'))
        self.assertTrue(select.validation(self.dbSchema))
        self.assertEqual(select.sorte(),[['id', 'name', 'age'], ['INTEGER', 'TEXT', 'INTERGER']])
        self.assertEqual(select.toSql(),"SELECT * FROM users WHERE id=0")
        #projection sur plusieurs colonne
        select = Select(Eq('name',Cst("Pierre")),Rel('users'))
        self.assertTrue(select.validation(self.dbSchema))
        self.assertEqual(select.sorte(),[['id', 'name', 'age'], ['INTEGER', 'TEXT', 'INTERGER']])
        self.assertEqual(select.toSql(),"SELECT * FROM users WHERE name=\"Pierre\"")

        select = Select(Eq('id',Cst(0)),Rel('us'))
        self.assertFalse(select.validation(self.dbSchema))

        select = Select(Eq('id',Cst('0')),Rel('users'))
        self.assertFalse(select.validation(self.dbSchema))

        select = Select(Eq('shitshit',Cst(0)),Rel('users'))
        self.assertFalse(select.validation(self.dbSchema))
    def test_Projection(self):
        proj = Proj(['id'],Rel('users'))
        self.assertTrue(proj.validation(self.dbSchema))
        self.assertEqual(proj.sorte(),[['id'], ['INTEGER']])
        self.assertEqual(proj.toSql(),"SELECT id FROM (users)")

        proj = Proj(['id','name'],Rel('users'))
        self.assertTrue(proj.validation(self.dbSchema))
        self.assertEqual(proj.sorte(),[['id', 'name'], ['INTEGER', 'TEXT']])
        self.assertEqual(proj.toSql(),"SELECT id,name FROM (users)")

        proj = Proj(['FAKECOL'],Rel('users'))
        self.assertFalse(proj.validation(self.dbSchema))
if __name__ == '__main__':
    unittest.main()
