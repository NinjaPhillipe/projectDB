import unittest
from operation import *

class MyTest(unittest.TestCase):
    dbSchema = DbSchema()
    dbSchema.tab = [['users', ['id', 'name', 'age'], ['INTEGER', 'TEXT', 'INTERGER']], ['annuaire', ['id', 'name', 'email', 'tel'], ['INTEGER', 'TEXT', 'TEXT', 'TEXT']]]
    def test_Cst(self):
        self.assertEqual(Cst(0).getType(),'INTEGER')
        self.assertEqual(Cst('0').getType(),'TEXT')
        self.assertEqual(Cst('rrrr').getType(),'TEXT')
        self.assertEqual(Cst(1.5).getType(),'REAL')
    def test_Rel(self):
        self.assertTrue(Rel('users').validation(self.dbSchema))
        ###########TEST_ERROR#################
        self.assertFalse(Rel('CC').validation(self.dbSchema))
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


        ###########TEST_ERROR#################
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

        ###########TEST_ERROR#################
        proj = Proj(['FAKECOL'],Rel('users'))
        self.assertFalse(proj.validation(self.dbSchema))
    def test_Union(self):
        rel1 = Rel("users")
        union = Union(rel1,rel1)
        self.assertTrue(union.validation(self.dbSchema))
        self.assertEqual(union.sorte(),rel1.sorte())

        union = Union(Select(Eq('id',Cst(0)),Rel('users')),Select(Eq('id',Cst(0)),Rel('users')))
        self.assertTrue(union.validation(self.dbSchema))
        ###########TEST_ERROR#################
        union = Union(Rel("users"),Rel("annuaire"))
        self.assertFalse(union.validation(self.dbSchema))

        union = Union(Select(Eq('id',Cst(0)),Rel('users')),Select(Eq('id',Cst(0)),Rel('annuaire')))
        self.assertFalse(union.validation(self.dbSchema))
    def test_Diff(self):
        rel1 = Rel("users")
        diff = Diff(rel1,rel1)
        self.assertTrue(diff.validation(self.dbSchema))
        self.assertEqual(diff.sorte(),rel1.sorte())
        ###########TEST_ERROR#################
        diff = Diff(Rel("users"),Rel("annuaire"))
        self.assertFalse(diff.validation(self.dbSchema))

        diff = Diff(Rel("users"),Rel("ERROR"))
        self.assertFalse(diff.validation(self.dbSchema))
    def test_Global(self):
        glob = Proj(['name'],Select(Eq('id',Cst(0)),Rel('users')))
        self.assertTrue(glob.validation(self.dbSchema))
        self.assertEqual(glob.sorte(),[['name'],['TEXT']])

        ###########TEST_ERROR#################
        #si la sous requete est mauvaise
        glob = Proj(['name'],Select(Eq('id',Cst('0')),Rel('users')))
        self.assertFalse(glob.validation(self.dbSchema))
if __name__ == '__main__':
    unittest.main()
