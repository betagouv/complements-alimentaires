## Fixtures

### Buts

Les fixtures sont utilisées dans les projets web pour pré-remplir la base de données avec des données initiales. Cela est utile pour :
- recréer instantanément sa propre base de données en cas de besoin (base "sale", migration appliquée problémtique, etc.)
- avoir des données en local qui ont volontairement des caractéristiques différentes, pour déceler d'éventuels soucis à l'usage (en plus des tests)
- partager ces données entre les différents développeurs (l'ajout d'une fixture étant versionnée, cela bénéficie à tous)
- permettre à un nouveau développeur d'avoir une base "remplie" juste après l'installation (y compris un compte admin)

Les fixtures sont utilisées dans les projets web pour pré-remplir la base de données avec des données initiales. Cela est utile pour :

- recréer instantanément sa propre base de données en cas de besoin (base "sale", migration appliquée problématique, besoin de créer une base adéquate en changeant de branche, etc.)
- avoir des données en local qui ont volontairement des caractéristiques différentes, pour déceler d'éventuels soucis à l'usage (en plus des tests)
- partager ces données entre les différents développeurs (l'ajout d'une fixture étant versionnée, cela bénéficie à tous)
- permettre à un nouveau développeur d'avoir une base "remplie" juste après l'installation (y compris un compte admin)
- à terme on peut imaginer des usages différents (hors environnement de dév) :
  - sur un environnement de démo : pour préparer des versions de démonstration de l'application
  - sur un environnement de staging/prod : préparer un import de données d'anciennes données

### Utilisation

- Django propose 2 commandes : `dumpdata` pour transformer la base actuelle en fichiers de fixtures, et `loaddata` pour injecter les fixtures dans la base.
- Nous avons simplement 2 commandes "chapeau" : `mydumpdata` et `myloaddata` à utiliser (cf. le code directement pour voir ce qu'elles font en plus).
