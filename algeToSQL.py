import unittest
from operation import *

eq = Eq('Country', Cst('Mali'))
print(eq.execute("TEST"))

rel = Rel('CC')
print(rel.execute("TEST"))

############################SELECT###############################
print("\n SELECT")
select = Select(eq,rel)
print(select.execute("TEST"))
select2 = Select(Eq("Money",Cst(100)),rel)
print(select2.execute("TEST"))
#ERROR
select3 = Select(eq,eq)
print(select3.execute("TEST"))
##########################PROJECTION#############################
print("\n PROJECTION")
proj = Proj(["Country","Money"],select)
print(proj.execute("TEST"))

proj2 = Proj(["Country","Money"],rel)
print(proj2.execute("TEST"))

#ERROR
proj3 = Proj(["Country","Money"],eq)
print(proj3.execute("TEST"))

#############################JOIN################################
print("\n JOIN")

############################RENAME###############################
print("\n RENAME")
rename = Rename("Country","Land",rel)
print(rename)

############################UNION################################
print("\n UNION")
union = Union(select,select)
print(union.execute("TEST"))
##########################DIFFERENCE#############################
print("\n DIFFERENCE")
diff = Diff(select,select)
print(diff.execute("TEST"))
############################Global###############################
print("\n GLOBAL")

# glob = Proj(["Population"],Join(Rename("Name", "Capital", Rel("Cities")),Select(Eq("Country", Cst("Mali")),Rel("CC"))))
# print(glob)


# class MyTest(unittest.TestCase):
#     def test(self):
#         ############################SELECT###############################
#         self.assertEqual(str(select),"SELECT * FROM CC WHERE Country = \"Mali\"")
#         self.assertEqual(str(select2),"SELECT * FROM CC WHERE Money = 100")
#         ##########################PROJECTION#############################
#         # self.assertEqual(str(),"SELECT Country,Money FROM (SELECT * FROM CC WHERE Country = \"Mali\")")
#
# if __name__ == '__main__':
#     unittest.main()
