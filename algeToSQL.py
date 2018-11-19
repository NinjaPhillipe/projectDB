import ast
import unittest
from operation import *

eq = Eq('Country', Cst('Mali'))
print(str(eq))

rel = Rel('CC')
print(rel)

############################SELECT###############################
print("\n SELECT")
select = Select(eq,rel)
# print(select)
select2 = Select(Eq("Money",100),rel)
# print(select2)
#ERROR
select3 = Select(eq,eq)
print(select3)
##########################PROJECTION#############################
print("\n PROJECTION")
proj = Proj(["Country","Money"],select)
print(proj)

proj2 = Proj(["Country","Money"],rel)
print(proj2)

#ERROR
proj3 = Proj(["Country","Money"],eq)
print(proj3)

#############################JOIN################################
print("\n JOIN")

############################RENAME###############################
print("\n RENAME")

############################UNION################################
print("\n UNION")
union = Union(select,select)
print(union)
##########################DIFFERENCE#############################
print("\n DIFFERENCE")
diff = Diff(select,select)
print(diff)

class MyTest(unittest.TestCase):
    def test(self):
        ############################SELECT###############################
        self.assertEqual(str(select),"SELECT * FROM CC WHERE Country = \"Mali\"")
        self.assertEqual(str(select2),"SELECT * FROM CC WHERE Money = 100")
        ##########################PROJECTION#############################
        # self.assertEqual(str(),"SELECT Country,Money FROM (SELECT * FROM CC WHERE Country = \"Mali\")")

if __name__ == '__main__':
    unittest.main()
