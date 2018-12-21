# Interpréteur de requête SPJRUD pour sqlite3

## Fonctionnement

Le module se découpe en plusieurs classes permettant de modéliser les requêtes algébriques SPJRUD.

#### `Cst()`

- une constante (une variable str int python)

#### `Rel()`

- un nom de table

#### `Eq()`

- un nom de colonne
- une constante ou une colonne

#### `Select()`

- un objet `Eq`
- un objet rel ou une sous requête

#### `Proj()`

- une liste de colonnes pour pour effectuer la projection
- un objet rel ou une sous requête

#### `Join()`

- un objet rel ou une sous requête
- un objet rel ou une sous requête

#### `Rename()`

- un objet rel ou une sous requête
- un objet rel ou une sous requête

#### `Union()`

- un objet rel ou une sous requête
- un objet rel ou une sous requête

#### `Diff()`

- un objet rel ou une sous requête
- un objet rel ou une sous requête

Pour modéliser une base de donnée on utilise la classe `BdSchema`.

## Manuel d'utilisation

Tout d'abord il faut créer un `DbSchema` et l'initialiser en ajoutant un schema personnel avec la variable ` db.tab=[table,[col1,col2],[type1,type2]] ` ou en prenant le schema d'une base de données sqlite3 avec la méthode `db.setDataBase(dbname) `.

ex :

`db = DbSchema()`

`db.setDataBase('dbname')`

Ensuite vous pouvez créer votre expression comme dans l'exemple ci dessous.

ex: `exp=Proj(['col1','col2'],Select(Eq(col,Cst('cst')),Rel('table')))`

Enfin vous pouvez vérifier la validité de la requête.
Manuellement avec la méthode `exp.validation(db)` pour valider votre requête et la méthode `exp.toSql()` pour récupérer la requête sql si l'expression est valide.

Vous pouvez aussi la valider automatiquement avec une `db.execute(query)` qui vérifie que la requête est valide et l’exécute sur la base de données sqlite3


/!\ Lors de la phase de validation si la requête n'est pas valide cela génère une `SpjrudToSqlException`
