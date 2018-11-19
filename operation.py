class Cst:
    type = ""
    """Objet representant une constante"""
    def __init__(self, name):
        # super(, self).__init__()
        self.name = name
    def __str__(self):
        if (self.name.isdigit()):
            return "{}".format(self.name)
        return "\"{}\"".format(self.name)
class Rel:
    """Objet representant une table"""
    type = "rel"
    #verifier par rapport a la base de donnée
    def __init__(self, table):
        # super(, self).__init__()
        self.table = table
    def __str__(self):
        return "{}".format(self.table)
class Eq:
    """Objet representant une egalité"""
    type = ""
    def __init__(self, col,constante):
        # super(, self).__init__()
        self.col = col
        self.constante = constante
    def __str__(self):
        return "{} = {}".format(self.col,self.constante)
class Select:
    """docstring for ."""
    type = "request"
    def __init__(self, eq,rel):
        # super(, self).__init__()
        self.eq = eq
        self.rel = rel
    def __str__(self):
        if(self.rel.type == "rel"):
            return "SELECT * FROM {1} WHERE {0}".format(str(self.eq),str(self.rel))
        else:
            return "ERROR Select"
class Proj:
    """docstring for ."""
    type = "request"
    def __init__(self, arrayCol,fff):
        # super(, self).__init__()
        self.arrayCol = arrayCol
        self.fff = fff
    def __str__(self):
        tmp = ""
        for t in self.arrayCol:
            if( tmp != ""):
                tmp+=","
            tmp+=t
        if (self.fff.type == "request"):
            return "SELECT {} FROM ({})".format(str(tmp),str(self.fff))
        elif(self.fff.type == "rel"):
            return "SELECT {} FROM {}".format(str(tmp),str(self.fff))
        else:
            return """ERROR {1} is not a valid argument \n ----> SELECT {0} FROM {1}""".format(str(tmp), str(self.fff))
class Join:
    """docstring for ."""
    type = "request"
    def __init__(self, exp1,exp2):
        # super(, self).__init__()
        self.exp1 = exp1
        self.exp2 = exp2
    def __str__(self):
        #si colonene en commun faire une intersection
        #sinon pas de colonne en commun faire union
        return "NotImplemented"
class Rename(object):
    """docstring for Rename."""
    def __init__(self, arg):
        # super(Rename, print("\n SELECT")self).__init__()
        self.arg = arg
    def __str__(self):
        return "RENAME NOTIMPLEMENTED"
class Union(object):
    """docstring for Union."""
    def __init__(self,exp1,exp2):
        # super(Union, self).__init__()
        self.exp1 = exp1
        self.exp2 = exp2
    def __str__(self):
        return "{} UNION {}".format(self.exp1,self.exp2)

class Diff:
    """docstring for ."""
    type = "request"
    def __init__(self, exp1,exp2):
        # super(, self).__init__()
        self.exp1 = exp1
        self.exp2 = exp2
    def __str__(self):
        return "{} EXCEPT {}".format(self.exp1,self.exp2)
