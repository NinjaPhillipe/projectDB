#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

class DbSchema:
    """docstring for DbSchema."""
    def __init__(self):
        # super(DbSchema, self).__init__()
        self.tab = []
    def setDataBase(self, dbname):
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
        self._sorte = None
    def getStructure(self):
        return self._structure
    def toRel(self):
        print("NOT IMPLEMENTED IN MAIN")
    def sorte(self):
        return self._sorte

class Cst(Main):
    """Objet representant une constante"""
    def __init__(self, name):
        # super().__init__()
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
    # _valid = True
    # verifier par rapport a la base de donnée
    def __init__(self, table):
        Main.__init__(self)
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
                self._structure = "{}".format(self.table)
                self._valid = True
                self._sorte = [table[1],table[2]]
                return True
        self._structure = "ERROR"
        return False
    # def getRelSchema(self,dbSchema):
    #     for table in dbSchema.getDbschema():
    #         if(table[0]==self.table):
    #             return tableT
    def toRel(self):
        return self
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
        # super().__init__()
        self._type = "request"
        self.eq ,self.rel = eq, rel
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
                            self._sorte = [table[1],table[2]]
                            self._structure = "SELECT * FROM {} WHERE {}".format(self.rel.table,str(self.eq))
                            self._valid = True
                            return True
        #on retourne le message d'erreur en focntion de l'ordre de verification
        if(not relValid):
            self._structure = "ERROR table does not exist"
        elif(not colValid):
            self._structure = "ERROR col does not exist"
        elif(not constanteValid):
            self._structure = "ERROR constante is not valid"
        return False
class Proj(Main):
    """docstring for ."""
    def __init__(self, arrayCol,rel):
        Main.__init__(self)
        self._type = "request"
        self.arrayCol = arrayCol
        self.rel = rel
    def validation(self,dbSchema):
        type = []
        for col in self.arrayCol:
            exist=False
            self.rel.validation(dbSchema)
            try:
                # si index() ne genere pas d'erreur alors la col fait partie de sorte()
                sorte = self.rel.toRel().sorte()
                index = sorte[0].index(col)
                type.append(sorte[1][index])
                self._valid = True
                tmp = ""
            except Exception as e:
                print("ERROR COL DOES NOT EXIST FOR PROJECTION")
                return False
        self._sorte = [self.arrayCol ,type]
        for t in self.arrayCol:
            if( tmp != ""):
                tmp+=","
            tmp+=t
        self.structure = "SELECT {} FROM ({})".format(str(tmp),self.rel._structure)
        return True
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
