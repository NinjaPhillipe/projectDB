import unittest
from operation import *

class MyTest(unittest.TestCase):
    dbSchema = DbSchema()
    #pour que les test reste valid meme si on modifie la base de donnée
    dbSchema.tab = [['annuaire', ['id', 'name', 'email', 'tel'], ['INTEGER', 'TEXT', 'TEXT', 'TEXT']],
                    ['users', ['id', 'firstname', 'age'], ['INTEGER', 'TEXT', 'INTEGER']],
                    ['job', ['id', 'job_name', 'sal'], ['INTEGER', 'TEXT', 'INTEGER']],
                    ['job_hiver', ['id', 'sal', 'job_name'], ['INTEGER', 'INTEGER', 'TEXT']]]

    def test_sorteEquality(self):
        self.assertTrue(sorteEquality([['id', 'firstname', 'age'], ['INTEGER', 'TEXT', 'INTEGER']],[['id', 'firstname', 'age'], ['INTEGER', 'TEXT', 'INTEGER']]))

        ###########TEST_ERROR#################
        self.assertFalse(sorteEquality([['id'], ['INTEGER']],[['id', 'firstname', 'age'], ['INTEGER', 'TEXT', 'INTEGER']]))
        self.assertFalse(sorteEquality([['id'], ['TEXT']],[['id'], ['INTEGER']]))
        self.assertFalse(sorteEquality([['id1'], ['INTEGER']],[['id'], ['INTEGER']]))
    def test_Cst(self):
        self.assertEqual(Cst(0).getType(),'INTEGER')
        self.assertEqual(Cst('0').getType(),'TEXT')
        self.assertEqual(Cst('rrrr').getType(),'TEXT')
        self.assertEqual(Cst(1.5).getType(),'REAL')
    def test_Rel(self):
        self.assertTrue(Rel('users').validation(self.dbSchema))
        rel = Rel("users")
        rel.validation(self.dbSchema)
        self.assertTrue(sorteEquality(rel.sorte(),[['id', 'firstname', 'age'], ['INTEGER', 'TEXT', 'INTEGER']]))
        ###########TEST_ERROR#################
        self.assertRaises(SpjrudToSqlException,lambda:Rel("CC").validation(self.dbSchema))
    def test_Select(self):
        #projection sur une colonne
        select = Select(Eq('id',Cst(0)),Rel('users'))
        self.assertTrue(select.validation(self.dbSchema))
        self.assertTrue(sorteEquality(select.sorte(),[['id', 'firstname', 'age'], ['INTEGER', 'TEXT', 'INTEGER']]))
        self.assertEqual(select.toSql(),"SELECT * FROM users WHERE id=0")
        #projection sur plusieurs colonne
        select = Select(Eq('firstname',Cst("Pierre")),Rel('users'))
        self.assertTrue(select.validation(self.dbSchema))
        self.assertTrue(sorteEquality(select.sorte(),[['id', 'firstname', 'age'], ['INTEGER', 'TEXT', 'INTEGER']]))
        self.assertEqual(select.toSql(),"SELECT * FROM users WHERE firstname=\"Pierre\"")


        ###########TEST_ERROR#################
        select = Select(Eq('id',Cst(0)),Rel('us'))
        self.assertRaises(SpjrudToSqlException,lambda:select.validation(self.dbSchema))
        select = Select(Eq('id',Cst('0')),Rel('users'))
        self.assertRaises(SpjrudToSqlException,lambda:select.validation(self.dbSchema))

        select = Select(Eq('shitshit',Cst(0)),Rel('users'))
        self.assertRaises(SpjrudToSqlException,lambda:select.validation(self.dbSchema))
    def test_Projection(self):
        proj = Proj(['id'],Rel('users'))
        self.assertTrue(proj.validation(self.dbSchema))
        self.assertEqual(proj.sorte(),[['id'], ['INTEGER']])
        self.assertEqual(proj.toSql(),"SELECT id FROM users")

        proj = Proj(['id','firstname'],Rel('users'))
        self.assertTrue(proj.validation(self.dbSchema))
        self.assertTrue(sorteEquality(proj.sorte(),[['id', 'firstname'], ['INTEGER', 'TEXT']]))
        self.assertEqual(proj.toSql(),"SELECT id,firstname FROM users")

        ###########TEST_ERROR#################
        proj = Proj(['FAKECOL'],Rel('users'))
        self.assertRaises(SpjrudToSqlException,lambda:proj.validation(self.dbSchema))
    def test_Join(self):
        join = Join(Rel("users"),Rel("annuaire"))
        self.assertTrue(join.validation(self.dbSchema))
        self.assertTrue(sorteEquality(join.sorte(),[['id', 'firstname', 'age', 'name', 'email', 'tel'], ['INTEGER', 'TEXT', 'INTEGER', 'TEXT', 'TEXT', 'TEXT']]))
        self.assertEqual(join.toSql(),"SELECT * FROM (SELECT * FROM users) NATURAL JOIN (SELECT * FROM annuaire)")

        ###########TEST_ERROR#################
        join = Join(Cst("OKOK"),Eq(10,12))
        self.assertFalse(join.validation(self.dbSchema))
    def test_Rename(self):
        rename = Rename("id","num",Rel("users"))
        self.assertTrue(rename.validation(self.dbSchema))
        self.assertTrue(sorteEquality(rename.sorte(),[['num', 'firstname', 'age'],['INTEGER','TEXT','INTEGER']]))
        self.assertTrue(sorteEquality(rename.toSql(),"SELECT id \"num\", firstname, age FROM users"))

        ###########TEST_ERROR#################
        rename = Rename("BLABLABLA","num",Rel("users"))
        self.assertRaises(SpjrudToSqlException,lambda:rename.validation(self.dbSchema))
        rename = Rename("id","num",Rel("BLABLABLA"))
        self.assertRaises(SpjrudToSqlException,lambda:rename.validation(self.dbSchema))
    def test_Union(self):
        rel1 = Rel("users")
        union = Union(rel1,rel1)
        self.assertTrue(union.validation(self.dbSchema))
        self.assertTrue(sorteEquality(union.sorte(),rel1.sorte()))
        self.assertEqual(union.toSql(),"SELECT * FROM (SELECT * FROM users) UNION SELECT id,firstname,age FROM users")

        union = Union(Select(Eq('id',Cst(0)),Rel('users')),Select(Eq('id',Cst(0)),Rel('users')))
        self.assertTrue(union.validation(self.dbSchema))

        union = Union(Rel("job"),Rel("job_hiver"))
        self.assertTrue(union.validation(self.dbSchema))
        self.assertEqual(union.toSql(),"SELECT * FROM (SELECT * FROM job) UNION SELECT id,job_name,sal FROM job_hiver" )
        ###########TEST_ERROR#################
        union = Union(Rel("users"),Rel("annuaire"))
        with self.assertRaises(Exception) as context:
            union.validation(self.dbSchema)
        self.assertTrue("Error row are not the same" in str(context.exception))

        union = Union(Select(Eq('id',Cst(0)),Rel('users')),Select(Eq('id',Cst(0)),Rel('annuaire')))
        with self.assertRaises(Exception) as context:
            union.validation(self.dbSchema)
        self.assertTrue("Error row are not the same" in str(context.exception))
    def test_Diff(self):
        rel1 = Rel("users")
        diff = Diff(rel1,rel1)
        self.assertTrue(diff.validation(self.dbSchema))
        self.assertTrue(sorteEquality(diff.sorte(),rel1.sorte()))
        self.assertEqual(diff.toSql(),"SELECT * FROM (SELECT * FROM users) EXCEPT SELECT id,firstname,age FROM users")
        diff = Diff(Rel("job"),Rel("job_hiver"))
        self.assertTrue(diff.validation(self.dbSchema))
        self.assertEqual(diff.toSql(),"SELECT * FROM (SELECT * FROM job) EXCEPT SELECT id,job_name,sal FROM job_hiver")

        ###########TEST_ERROR#################
        diff = Diff(Rel("users"),Rel("annuaire"))
        print(diff.validation(self.dbSchema))
        # self.assertRaises(SpjrudToSqlException,lambda:diff.validation(self.dbSchema))

        diff = Diff(Rel("users"),Rel("ERROR"))
        self.assertRaises(SpjrudToSqlException,lambda:diff.validation(self.dbSchema))
    def test_Global(self):
        glob = Proj(['firstname'],Select(Eq('id',Cst(0)),Rel('users')))
        self.assertTrue(glob.validation(self.dbSchema))
        self.assertTrue(sorteEquality(glob.sorte(),[['firstname'],['TEXT']]))
        self.assertEqual(glob.toSql(),"SELECT firstname FROM (SELECT * FROM users WHERE id=0)")

        req = Rename('firstname','Employee' ,Proj(['firstname'],Select(Eq('id',Cst(0)),Rel('users'))))
        req2 = Select(Eq('id',Cst(0)),Rel('users'))
        req3 = Join(req,req2)
        self.assertTrue(req3.validation(self.dbSchema))
        self.assertTrue(sorteEquality(req3.sorte(),[['Employee', 'id', 'firstname', 'age'], ['TEXT', 'INTEGER', 'TEXT', 'INTEGER']]))

        glob= Select(Eq("id",Cst(0)),Proj(["firstname","id"],Rel("users")))
        self.assertTrue(glob.validation(self.dbSchema))
        self.assertTrue(sorteEquality(glob.sorte(),[['firstname', 'id'], ['TEXT', 'INTEGER']]))
        self.assertEqual(glob.toSql(),"SELECT * FROM (SELECT firstname,id FROM users) WHERE id=0")
        ###########TEST_ERROR#################
        #si la sous requete est mauvaise
        glob = Proj(['firstname'],Select(Eq('id',Cst('0')),Rel('users')))
        self.assertRaises(SpjrudToSqlException,lambda:glob.validation(self.dbSchema))
if __name__ == '__main__':
    unittest.main()
