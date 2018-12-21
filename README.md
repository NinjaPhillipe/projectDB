# Interpréteur de requête SPJRUD pour sqlite3

## Structure

Le module se découpe en plusieurs classes permettant de modéliser les requêtes algébriques SPJRUD.

* `Cst()`
* `Rel()`
* `Eq()`
* `Select()`
* `Proj()`
* `Join()`
* `Rename()`
* `Union()`
* `Diff()`

Pour modéliser une base de donnée on utilise la classe BdSchema.

## Manuel d'utilisation

Tout d'abord il faut créer un `DbSchema` et l'initialiser en ajoutant un schema personnel avec la méthode `  ` ou avec le schema d'une base de données sqlite3 avec la méthode ` `.

ex :

`db = DbSchema()`

`db.setDataBase('dbname')`

Ensuite vous pouvez créer votre expression comme dans l'exemple ci dessous.

ex: `exp=Proj(['col1','col2'],Select(Eq(col,Cst('cst')),Rel('table')))`

Enfin vous pouvez vérifier la validité de la requête.
Manuellement avec la méthode `exp.validation(db)` pour valider votre requête et la méthode `exp.toSql()` pour récupérer la requête sql si l'expression est valide.




/!\ Lors de la phase de validation  
