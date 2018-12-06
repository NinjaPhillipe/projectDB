class DbSchema:
    """docstring for DbSchema."""
    def __init__(self, db):
        # super(DbSchema, self).__init__()
        tables = []
        # getDbshema(db)

    def getDbshema(self,db):
        print("test")
    # def add_table(self,tableName,colName,colType):



class Table:
    """docstring for table."""
    def __init__(self, tableName,colName,colType):
        # super(table, self).__init__()
        self.name = tableName
        self.colName = colName
        self.colType = colType


class Cst:
    """Objet representant une constante"""
    valid = True
    type = ""
    def __init__(self, name):
        # super(, self).__init__()
        self.name = str(name)
    def execute(self, db):
        if (self.name.isdigit()):
            return "{}".format(self.name)
        return "\"{}\"".format(self.name)

class Rel:
    """Objet representant une table"""
    type = "rel"
    valid = True
    #verifier par rapport a la base de donnée
    def __init__(self, table):
        # super(, self).__init__()
        self.table = table
    def execute(self,db):
        return "{}".format(self.table)
class Eq:
    """Objet representant une egalité"""
    type = "eq"
    valid = True
    def __init__(self, col,constante):
        # super(, self).__init__()
        self.col = col
        self.constante = constante
    def execute(self,db):
        return "{} = {}".format(self.col,self.constante.execute(db))
class Select:
    """docstring for ."""
    type = "request"
    valid = True
    request = "ERROR"
    def __init__(self, eq,rel):
        # super(, self).__init__()
        self.eq = eq
        self.rel = rel
    def execute(self, db):
        if(self.rel.type == "rel" and self.eq.type == "eq"):
            self.request = "SELECT * FROM {1} WHERE {0}".format(self.eq.execute(db),self.rel.execute(db))
        else:
            self.request = "Error invalid argument type"
            self.valid = False
        return self.request

class Proj:
    """docstring for ."""
    type = "request"
    valid = True
    def __init__(self, arrayCol,fff):
        # super(, self).__init__()
        self.arrayCol = arrayCol
        self.fff = fff
    def execute(self,db):
        tmp = ""
        for t in self.arrayCol:
            if( tmp != ""):
                tmp+=","
            tmp+=t
        if (self.fff.type == "request"):
            return "SELECT {} FROM ({})".format(str(tmp),self.fff.execute(db))
        elif(self.fff.type == "rel"):
            return "SELECT {} FROM {}".format(str(tmp),self.fff.execute(db))
        else:
            return """ERROR {1} is not a valid argument \n ----> SELECT {0} FROM {1}""".format(str(tmp), self.fff.execute(db))
class Join:
    """docstring for ."""
    type = "join"
    valid = True
    def __init__(self, exp1,exp2):
        # super(, self).__init__()
        self.exp1 = exp1
        self.exp2 = exp2
    def __str__(self):
        #si colonene en commun faire une intersection
        #sinon pas de colonne en commun faire union
        return "SELECT * FROM ({0}) INNER JOIN ON (({0}).key = ({1}).key)".format(self.exp1,self.exp2)
class Rename: #incorrect
    """docstring for Rename."""
    type = "rename"
    valid = True
    def __init__(self, col,newName,table):
        # super(Rename, print("\n SELECT")self).__init__()
        self.col = col
        self.newName = newName
        self.table = table
    def __str__(self):
        return "SELECT {} \"{}\" FROM {}".format(self.col,self.newName,self.table)
class Union:
    """docstring for Union."""
    type = "union"
    valid = True
    def __init__(self,exp1,exp2):
        # super(Union, self).__init__()
        self.exp1 = exp1
        self.exp2 = exp2
    def execute(self,db):
        # print(self.exp1.execute(db))
        return "{} UNION {}".format(self.exp1.execute(db),self.exp2.execute(db))

    # def __str__(self):
    #     return "{} UNION {}".format(self.exp1.execute(db).,self.exp2.execute(db))

class Diff:
    """docstring for ."""
    type = "diff"
    valid = True
    def __init__(self, exp1,exp2):
        # super(, self).__init__()
        self.exp1 = exp1
        self.exp2 = exp2
    def execute(self,db):
        return "{} EXCEPT {}".format(self.exp1.execute(db),self.exp2.execute(db))
