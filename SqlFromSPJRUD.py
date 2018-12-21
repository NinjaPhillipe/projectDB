#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

def sorteEquality(sorte1,sorte2):
    for col in sorte1[0]:     #verificaton de l'égalité par double inclusion
        if(not col in sorte2[0]):
            return False
        if(not sorte1[1][sorte1[0].index(col)] == sorte2[1][sorte2[0].index(col)]):#plus verifier si les types des colonnes sont egaux
            return False # type colonne incorrect
    for col in sorte2[0]:
        if(not col in sorte1[0]):
            return False
        if(not sorte1[1][sorte1[0].index(col)] == sorte2[1][sorte2[0].index(col)]):
            return False # type colonne incorrect
    return True
class SpjrudToSqlException(Exception):
    """SpjrudToSqlException est une exception pour reconnaitre les exceptions générées volontairement par le programme."""
    pass

class DbSchema:
    """docstring for DbSchema."""
    def __init__(self):
        self.tab = []
        self.trueDB=False
    def setDataBase(self, dbname):
        self.dbname = dbname
        try:
            self.db = sqlite3.connect(self.dbname)
            for table in self.getTables():
                self.getColInfo(table)
            self.trueDB = True
        except Exception as e:
            raise e
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
    def execute(self,query,printQuery=False):
        if(not self.trueDB):
            print("NOT TRUE DB")
            return False
        if(not query.validation(self)):
            print("Query is not valid : ")
            return False
        if(printQuery):
            print(query.toSql())
        cur = self.db.cursor()
        cur.execute(query.toSql())
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return True
    def createTable(self,name,query):
        if(not self.trueDB):
            print("NOT TRUE DB")
            return False
        if(not query.validation(self)):
            print("Query is not valid : ")
            return False
        cur = self.db.cursor()
        cur.execute("CREATE TABLE {} AS {}".format(name,query.toSql()))
        rows = cur.fetchall()

class Main:
    """Classe qui sert de schema pour les autres"""
    def __init__(self):
        self._structure=None
        self._error=None
        self._valid=False
        self._type="UNVALIDTYPE"
        self._sorte = None
    def getStructure(self):
        return self._structure
    def sorte(self):
        return self._sorte
    def toSql(self):
        return self._structure
    def getType(self):
        return self._type
    def __add__(rel1, rel2):
        return Union(rel1,rel2)
    def __sub__(rel1, rel2):
        return Diff(rel1,rel2)

class Cst:
    """Objet representant une constante"""
    def __init__(self, name):
        self.name = name
        self._type = ""
        if (isinstance(self.name, int)):
            self._valid=True
            self._type='INTEGER'
        elif (isinstance(self.name, float)):
            self._valid=True
            self._type='REAL'
        elif (isinstance(self.name, str)):
            self._valid=True
            self._type="TEXT"
        else :
            raise SpjrudToSqlException("Invalid type or not support by this prog")
    def validation(self, dbSchema):
        return true
    def getType(self):
        return self._type

class Rel(Main):
    """Objet representant une table"""
    # _valid = True
    # verifier par rapport a la base de donnée
    def __init__(self, name):
        Main.__init__(self)
        self._type = "rel"
        self._name = name
    def validation(self,dbSchema):
        #vérifie si la table existe
        for table in dbSchema.getDbschema():
            if(table[0]==self._name):
                self._structure = "{}".format(self._name)
                self._valid = True
                self._sorte = [table[1],table[2]]
                return True
        raise SpjrudToSqlException("\n ERROR: table {0} does not exist in Rel(\"{0}\")".format(self._name))
        return False
    def toSql(self):
        return "SELECT * FROM {}".format(self._name)
    def getSPJRUD(self):
        return str(self._name)

class Eq:
    """Objet representant une egalité"""
    def __init__(self, col,constante):
        self._type = "eq"
        self.col = col
        self.constante = constante
    def validation(self,dbSchema):
        self._structure =  "{} = {}".format(self.col,self.constante.validation(dbSchema))
        return True
    def getSPJRUD(self):
        if(type(self.constante)==str):
            return "Eq({},{})".format(self.col,self.constante)
        return "Eq({},{})".format(self.col,self.constante.name)
    def __str__(self):
        if(type(self.constante)==str):
            return self.col +"="+str(self.constante)
        elif(self.constante.getType()=="TEXT"):
            return self.col +"=\""+str(self.constante.name)+"\""
        else:
            return self.col +"="+str(self.constante.name)
class Select(Main):
    """docstring for ."""
    def __init__(self, eq,rel):
        Main.__init__(self)
        self._type = "select"
        self.eq ,self.rel = eq, rel
    def validation(self, dbSchema):
        #on retourne le message d'erreur en focntion de l'ordre de verification
        if(not self.rel.validation(dbSchema)): #la recursivité va tomber sur l'erreur et la raise
            return "ERROR SUB REQUEST" # On a un return par sécurité
        if(not self.eq.col in self.rel.sorte()[0]): # si la colonne n'est pas dans le schema
            raise SpjrudToSqlException("ERROR in {} \n col {} does not exist in {}".format(self.getSPJRUD(),self.eq.col,self.rel.sorte()))
        if(type(self.eq.constante)==Cst): #si c'est une constante
            if(not self.eq.constante.getType()== self.rel.sorte()[1][self.rel.sorte()[0].index(self.eq.col)] ): # si le type de la colonne n'est pas egale au type de la constante
                raise SpjrudToSqlException("ok")
        else: # sinon c'est une colonne
            if(not self.eq.constante in self.rel.sorte()[0]): #si la colonne n'est pas dans le schema
                raise SpjrudToSqlException("ERROR in {} \n col {} does not exist in {}".format(self.getSPJRUD(),self.eq.constante,self.rel.sorte()))
            if(not self.rel.sorte()[1][self.rel.sorte()[0].index(self.eq.constante)]== self.rel.sorte()[1][self.rel.sorte()[0].index(self.eq.col)] ): # si les types des colonnes ne sont pas egaux
                raise SpjrudToSqlException("ERROR in {} \n type of column {} and {} are not equals {} != {}".format(self.getSPJRUD(),self.eq.col,self.eq.constante,self.rel.sorte()[1][self.rel.sorte()[0].index(self.eq.col)],self.rel.sorte()[1][self.rel.sorte()[0].index(self.eq.constante)]))
        if(self.rel.getType() == "rel"):
            self._structure = "SELECT * FROM {} WHERE {}".format(self.rel._name,str(self.eq))
        else:
            self._structure = "SELECT * FROM ({}) WHERE {}".format(self.rel.toSql(),str(self.eq))
        self._valid = True
        return True
    def getSPJRUD(self):
        return "Select({},{})".format(self.eq.getSPJRUD(),self.rel.getSPJRUD())
    def sorte(self):
        if(self._valid):
            return self.rel.sorte()

class Proj(Main):
    """docstring for ."""
    def __init__(self, arrayCol,rel):
        Main.__init__(self)
        self._type = "request"
        self.arrayCol = arrayCol
        self.rel = rel
    def validation(self,dbSchema):
        type = []
        if(not self.rel.validation(dbSchema)):
            return "ERROR SUB REQUEST"
        projCol=""
        for col in self.arrayCol:
            if(not col in self.rel.sorte()[0]):
                raise SpjrudToSqlException("ERROR in {} \n column {} does not exist in {}".format(self.getSPJRUD(),col,self.rel.sorte()[0]))
                return False
            if(projCol==""):
                projCol +=col
            else:
                projCol +=",{}".format(col)
        if(self.rel.getType() == "rel"):
            self._structure = "SELECT {} FROM {}".format(projCol,self.rel._structure)
        else:
            self._structure = "SELECT {} FROM ({})".format(projCol,self.rel._structure)
        self._valid = True
        return True
    def sorte(self):
        if(self._valid):
            res= [[],[]]
            for col in self.arrayCol:
                res[0].append(col)
                res[1].append(self.rel.sorte()[1][self.rel.sorte()[0].index(col)])
            return res
    def getSPJRUD(self):
        return "Proj({},{})".format(self.arrayCol,self.rel.getSPJRUD())

class Join(Main):
    """docstring for ."""
    def __init__(self, exp1,exp2):
        Main.__init__(self)
        self._type = "join"
        self.exp1 = exp1
        self.exp2 = exp2
    def validation(self,dbSchema):
        if(not (self.exp1.validation(dbSchema) and self.exp2.validation(dbSchema))):
            return "ERROR SUB REQUEST"
        self._valid = True
        self._structure = "SELECT * FROM ({}) NATURAL JOIN ({})".format(self.exp1.toSql(),self.exp2.toSql())
        return True
    def sorte(self):
        if(self._valid):
            res = [[],[]]
            for col in self.exp1.sorte()[0]:
                res[0].append(col)
                res[1].append(self.exp1.sorte()[1][self.exp1.sorte()[0].index(col)])
            for col in self.exp2.sorte()[0]: #ajoute les col si elles ne sont pas dans res
                if(not col in res[0]):
                    res[0].append(col)
                    res[1].append(self.exp2.sorte()[1][self.exp2.sorte()[0].index(col)])
            return res
    def getSPJRUD(self):
        return "Join({},{})".format(self.exp1.getSPJRUD(),self.exp2.getSPJRUD())

class Rename(Main):
    """docstring for Rename."""
    def __init__(self, col,newName,rel):
        Main.__init__(self)
        self._type = "rename"
        self.col = col
        self.newName = newName
        self.rel = rel
    def validation(self,dbSchema):
        if(not self.rel.validation(dbSchema)):
            return "ERROR SUB REQUEST"
        if(not self.col in self.rel.sorte()[0]):
            raise SpjrudToSqlException("ERROR in {} \n col {} is not in {}".format(self.getSPJRUD(),self.col,self.rel.sorte()[0]))
            return False
        if(self.newName in self.rel.sorte()[0]):
            raise SpjrudToSqlException("ERROR in {} \n new name {} is already in {}".format(self.getSPJRUD(),self.newName,self.rel.sorte()[0]))
            return False
        if(self.rel.getType()=="rel"):
            self._structure = "SELECT {} AS {} FROM {}".format(self.col,self.newName,self.rel._name)
        else:
            self._structure = "SELECT {} AS {} FROM ({})".format(self.col,self.newName,self.rel.toSql())
        self._valid=True
        return True
    def sorte(self):
        if(self._valid):
            index = self.rel.sorte()[0].index(self.col)# car col est dans sorte() car la requete est valid
            res=[[],[]]
            for i in range(len(self.rel.sorte()[0])): #deepcopy
                res[0].append(self.rel.sorte()[0][i])
                res[1].append(self.rel.sorte()[1][i])
            res[0][index] = self.newName
            return res
    def getSPJRUD(self):
        return "Rename({},{},{})".format(self.col,self.newName,self.rel.getSPJRUD())

class Union(Main):
    """docstring for Union."""
    def __init__(self,exp1,exp2):
        Main.__init__(self)
        self._type = "union"
        self.exp1 = exp1
        self.exp2 = exp2
    def validation(self,dbSchema):
        if(not (self.exp1.validation(dbSchema) and self.exp2.validation(dbSchema))):
            return "ERROR SUB REQUEST"
        if(not sorteEquality(self.exp1.sorte(),self.exp2.sorte())):
            raise SpjrudToSqlException("Error in {} \n row are not the same {}!={}".format(self.getSPJRUD(),self.exp1.sorte(),self.exp2.sorte()))
        unionCol=""
        for col in self.exp1.sorte()[0]:
            if(unionCol==""):
                unionCol +=col
            else:
                unionCol +=",{}".format(col)
        if(self.exp2.getType() == "rel"):
            self._structure = "SELECT * FROM ({}) UNION SELECT {} FROM {}".format(self.exp1.toSql(),unionCol,self.exp2._name)
        else:
            self._structure = "SELECT * FROM ({}) UNION SELECT {} FROM ({})".format(self.exp1.toSql(),unionCol,self.exp2.toSql())
        self._valid=True
        return True

    def sorte(self):
        if(self._valid):
            return self.exp1.sorte()
    def getSPJRUD(self):
        return "Union({},{})".format(self.exp1.getSPJRUD(),self.exp2.getSPJRUD())

class Diff(Main):
    """docstring for Diff"""
    def __init__(self, exp1,exp2):
        Main.__init__(self)
        self._type = "diff"
        self.exp1 = exp1
        self.exp2 = exp2
    def validation(self,dbSchema):
        if(not (self.exp1.validation(dbSchema) and self.exp2.validation(dbSchema))):
            return "ERROR SUB REQUEST"
        if(not sorteEquality(self.exp1.sorte(),self.exp2.sorte())):
            raise SpjrudToSqlException("Error in {} \n row are not the same {}!={}".format(self.getSPJRUD(),self.exp1.sorte(),self.exp2.sorte()))
        exceptCol=""
        for col in self.exp1.sorte()[0]:
            if(exceptCol==""):
                exceptCol +=col
            else:
                exceptCol +=",{}".format(col)
        if(self.exp2.getType() == "rel"):
            self._structure = "SELECT * FROM ({}) EXCEPT SELECT {} FROM {}".format(self.exp1.toSql(),exceptCol,self.exp2._name)
        else:
            self._structure = "SELECT * FROM ({}) EXCEPT SELECT {} FROM ({})".format(self.exp1.toSql(),exceptCol,self.exp2.toSql())
        self._valid=True
        return True
    def sorte(self):
        if(self._valid):
            return self.exp1.sorte()
    def getSPJRUD(self):
        return "Diff({},{})".format(self.exp1.getSPJRUD(),self.exp2.getSPJRUD())
