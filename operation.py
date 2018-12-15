import sqlite3

class DbSchema:
    """docstring for DbSchema."""
    def __init__(self, dbname):
        # super(DbSchema, self).__init__()
        self.tab = []
        self.tables = []
        self.dbname = dbname
        self.db = sqlite3.connect(self.dbname)
        for table in self.getTables():
            self.getColInfo(table)
    def getDbschema(self):
        return self.tab
    def getTables(self):
        cursor = self.db.cursor()
        tablesName = []
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for tuple in cursor.fetchall():
            if(tuple[0] != "sqlite_sequence"):
                tablesName.append(tuple[0])
        return tablesName

    def getColInfo(self,table):
        colName = []
        colType = []
        cursor = self.db.cursor()
        for col in cursor.execute("PRAGMA table_info({})".format(table)).fetchall():
            colName.append(col[1])
            colType.append(col[2])
        self.tab.append([table,colName,colType])
    def __str__(self):
        #format [table, colonoe, type]
        return str(self.tab)

class Main:
    """docstring for main."""
    def __init__(self):
        self._structure="CRITICALERROR"
        self._valid=False
        self._type="UNVALIDTYPE"
    def isValid(self):
        return self._valid

class Cst(Main):
    """Objet representant une constante"""
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.type = ""
        if (isinstance(self.name, int)):
            self._valid=True
            self.type='INTEGER'
        elif (isinstance(self.name, float)):
            self._valid=True
            self.type='REAL'
        elif (isinstance(self.name, str)):
            self._valid=True
            self.type="TEXT"
        else :
            return "ERROR"
    def validation(self, dbSchema):
        pass
        # if (self.name.isdigit()):
        #     return "{}".format(self.name)
        # return "\"{}\"".format(self.name)

class Rel(Main):
    """Objet representant une table"""
    _valid = True
    #verifier par rapport a la base de donnée
    def __init__(self, table):
        super().__init__()
        self._type = "rel"
        self.table = table
    def __add__(rel1, rel2):
        return Union(rel1,rel2)
    def __sub__(rel1, rel2):
        return Diff(rel1,rel2)

    def validation(self,dbSchema):
        #vérifie si la table existe
        for table in dbSchema.getDbschema():
            if(table[0]==self.table):
                return "{}".format(self.table)
        return "ERROR"
    def getRelSchema(self,dbSchema):
        for table in dbSchema.getDbschema():
            if(table[0]==self.table):
                return table
class Eq:
    """Objet representant une egalité"""
    def __init__(self, col,constante):
        self._type = "eq"
        self.col = col
        self.constante = constante
    def validation(self,dbSchema):
        return "{} = {}".format(self.col,self.constante.validation(dbSchema))
    def __str__(self):
        return self.col +"="+str(self.constante.name)
class Select(Main):
    """docstring for ."""
    def __init__(self, eq,rel):
        super().__init__()
        self._type = "request"
        self.eq = eq
        self.rel = rel
    def validation(self, dbSchema):
        relValid,colValid,constanteValid=False,False,False
        for table in dbSchema.getDbschema():
            if(table[0]==self.rel.table): #on verifie si la table existe dans la base de donnée
                relValid=True
                for col in table[1]:
                    if(self.eq.col == col): #on vérifie si colone existe
                        colValid=True
                        index = table[1].index(col) #on récupere l'indice de la col
                        if(self.eq.constante.type==table[2][index]): #type consatnte == type de la colonne
                            constanteValid=True
                            self._valid =True
                            return "SELECT * FROM {0} WHERE {1}".format(self.rel.table,str(self.eq))
        #on retourne le message d'erreur en focntion de l'ordre de verification
        if(not relValid):
            return "ERROR table does not exist"
        elif(not colValid):
            return "ERROR col does not exist"
        elif(not constanteValid):
            return "ERROR constante is not valid"
class Proj:
    """docstring for ."""
    def __init__(self, arrayCol,fff):
        # super(, self).__init__()
        self._type = "request"
        self.arrayCol = arrayCol
        self.fff = fff
    def validation(self,dbSchema):
        for col in arrayCol:
            print("NOT MPLEMENTED")
        # tmp = ""
        # for t in self.arrayCol:
        #     if( tmp != ""):
        #         tmp+=","
        #     tmp+=t
        # if (self.fff.type == "request"):
        #     return "SELECT {} FROM ({})".format(str(tmp),self.fff.validation(dbSchema))
        # elif(self.fff.type == "rel"):
        #     return "SELECT {} FROM {}".format(str(tmp),self.fff.validation(dbSchema))
        # else:
        #     return """ERROR {1} is not a valid argument \n ----> SELECT {0} FROM {1}""".format(str(tmp), self.fff.validation(dbSchema))
class Join:
    """docstring for ."""
    def __init__(self, exp1,exp2):
        # super(, self).__init__()
        self._type = "join"
        self.exp1 = exp1
        self.exp2 = exp2
    def __str__(self):
        #si colonene en commun faire une intersection
        #sinon pas de colonne en commun faire union
        return "SELECT * FROM ({0}) INNER JOIN ON (({0}).key = ({1}).key)".format(self.exp1,self.exp2)
class Rename: #incorrect
    """docstring for Rename."""
    def __init__(self, col,newName,table):
        # super(Rename, print("\n SELECT")self).__init__()
        self._type = "rename"
        self.col = col
        self.newName = newName
        self.table = table
    def __str__(self):
        return "SELECT {} \"{}\" FROM {}".format(self.col,self.newName,self.table)
class Union:
    """docstring for Union."""
    def __init__(self,exp1,exp2):
        # super(Union, self).__init__()
        self._type = "union"
        self.exp1 = exp1
        self.exp2 = exp2
    def validation(self,dbSchema):
        # print(self.exp1.validation(dbSchema))
        return "{} UNION {}".format(self.exp1.validation(dbSchema),self.exp2.validation(dbSchema))

    # def __str__(self):
    #     return "{} UNION {}".format(self.exp1.validation(dbSchema).,self.exp2.validation(dbSchema))

class Diff:
    """docstring for ."""
    def __init__(self, exp1,exp2):
        # super(, self).__init__()
        self._type = "diff"
        self.exp1 = exp1
        self.exp2 = exp2
    def validation(self,dbSchema):
        return "{} EXCEPT {}".format(self.exp1.validation(dbSchema),self.exp2.validation(dbSchema))
