import ast
from operation import *

eq = Eq('Country', Cst('Mali'))
rel = Rel('CC')
test = Select(eq,rel)

print(str(eq))
print(rel)
print(test)
