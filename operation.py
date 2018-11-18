class Cst:
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
    #verifier par rapport a la base de donnée
    def __init__(self, table):
        # super(, self).__init__()
        self.table = table
    def __str__(self):
        return "{}".format(self.table)
class Eq:
    """Objet representant une egalité"""
    def __init__(self, col,constante):
        # super(, self).__init__()
        self.col = col
        self.constante = constante
    def __str__(self):
        return "{} = {}".format(self.col,self.constante)
class Join:
    """docstring for ."""
    def __init__(self, arg):
        # super(, self).__init__()
        self.arg = arg
    def __str__(self):
        return "NotImplemented"
class Projection:
    """docstring for ."""
    def __init__(self, ArrayCol):
        # super(, self).__init__()
        self.arrayCol = ArrayCol
    def __str__(self):
        return "NotImplemented"
class Select:
    """docstring for ."""
    def __init__(self, eq,rel):
        # super(, self).__init__()
        self.eq = eq
        self.rel = rel
    def __str__(self):
        return "SELECT * FROM {1} WHERE {0}".format(str(self.eq),str(self.rel))
class Diff:
    """docstring for ."""
    def __init__(self, arg):
        # super(, self).__init__()
        self.arg = arg
    def __str__(self):
        return "NotImplemented"
