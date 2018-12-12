import sqlite3

class DbSchema:
    """docstring for DbSchema."""
    def __init__(self, dbname):
        # super(DbSchema, self).__init__()
        self.tables = []
        self.dbname = dbname
        self.db = sqlite3.connect(self.dbname)
    def getDbschema(self):
        for table in self.getTables():
            self.getColInfo(table)

    def getTables(self):
        cursor = self.db.cursor()
        tablesName = []
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for tuple in cursor.fetchall():
            if(tuple[0] != "sqlite_sequence"):
                tablesName.append(tuple[0])
        return tablesName

    def getColInfo(self,table):
        print("__________",table,"____________")
        colName = []
        colType = []
        cursor = self.db.cursor()
        for col in cursor.execute("PRAGMA table_info('annuaire')").fetchall():
            colName.append(col[1])
            colType.append(col[2])
        print(table,colName,colType)


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
    def execute(self, dbSchema):
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
    def execute(self,dbSchema):
        return "{}".format(self.table)
class Eq:
    """Objet representant une egalité"""
    type = "eq"
    valid = True
    def __init__(self, col,constante):
        # super(, self).__init__()
        self.col = col
        self.constante = constante
    def execute(self,dbSchema):
        return "{} = {}".format(self.col,self.constante.execute(dbSchema))
class Select:
    """docstring for ."""
    type = "request"
    valid = True
    request = "ERROR"
    def __init__(self, eq,rel):
        # super(, self).__init__()
        self.eq = eq
        self.rel = rel
    def execute(self, dbSchema):
        if(self.rel.type == "rel" and self.eq.type == "eq"):
            self.request = "SELECT * FROM {1} WHERE {0}".format(self.eq.execute(dbSchema),self.rel.execute(dbSchema))
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
    def execute(self,dbSchema):
        tmp = ""
        for t in self.arrayCol:
            if( tmp != ""):
                tmp+=","
            tmp+=t
        if (self.fff.type == "request"):
            return "SELECT {} FROM ({})".format(str(tmp),self.fff.execute(dbSchema))
        elif(self.fff.type == "rel"):
            return "SELECT {} FROM {}".format(str(tmp),self.fff.execute(dbSchema))
        else:
            return """ERROR {1} is not a valid argument \n ----> SELECT {0} FROM {1}""".format(str(tmp), self.fff.execute(dbSchema))
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
    def execute(self,dbSchema):
        # print(self.exp1.execute(dbSchema))
        return "{} UNION {}".format(self.exp1.execute(dbSchema),self.exp2.execute(dbSchema))

    # def __str__(self):
    #     return "{} UNION {}".format(self.exp1.execute(dbSchema).,self.exp2.execute(dbSchema))

class Diff:
    """docstring for ."""
    type = "diff"
    valid = True
    def __init__(self, exp1,exp2):
        # super(, self).__init__()
        self.exp1 = exp1
        self.exp2 = exp2
    def execute(self,dbSchema):
        return "{} EXCEPT {}".format(self.exp1.execute(dbSchema),self.exp2.execute(dbSchema))
