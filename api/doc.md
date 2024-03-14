# Documentation sur l'API

### Gestion personnalisée des erreurs

#### Pourquoi ?

Il est nécessaire de personnaliser les erreurs afin de :
- Pouvoir lever une exception en 1 ligne dans nos endpoints
- Transmettre au front-end la manière dont devrait être afficher cette erreur (globalement dans un toast, ou sur un champ spécifique d'un formulaire par exemples)

#### Fonctionnement des erreurs avec DRF

- DRF dispose d'un mécanisme natif de gestion d'exceptions sur lequel nous nous appuyons pour ne pas réinventer la roue. Il dispose de la classe `APIException` dont hérite de nombreuses erreurs standards comme par exemple `MethodNotAllowed` ou `AuthenticationFailed`
- DRF propose d'utilise un custom handler : une fonction qui sera appelée dès qu'une exception est levée dans un endpoint, pour nous permettre de personnaliser la réponse à ce moment.

#### Ce qu'on ajoute

- Nous créeons une classe d'exception `ProjectAPIException` abstraite, qui hérite de la classe DRF `APIException`, avec un code 400.
- Nous pouvons ensuite créer des exceptions personnalisées qui héritent de `ProjectAPIException` et doivent définir en plus comment afficher l'erreur. Par exemple :

```python
class EmailAlreadyExists(ProjectAPIException):
    default_detail = "L'adresse e-mail renseignée existe déjà."
    display = "field"
    field_name = "email"

raise EmailAlreadyExists # dans un endpoint
```

- Note : Les champs de ces classes peuvent aussi être modifiées à l'instanciation, par exemple pour modifier le nom du champ. Par exemple :

```python
...
raise EmailAlreadyExists(field_name="new_email")
```

- La méthode `custom_exception_handler` gère les exceptions qui arrivent et injecte dans la réponse les différents champs attendus.

- Un message d'erreur peut aussi contenir des valeurs dynamiques, par exemple :

```python
class EmailAlreadyExists(ProjectAPIException):
    default_detail = "L'addresse {given_email} existe déjà."
    display = "field"
    field_name = "email"

raise EmailAlreadyExists(given_email=email)
```

- Chaque ProjectAPIException écrit un log de level "INFO" par défaut. Cela peut être changé. Par exemple :

```python
raise EmailAlreadyExists(log_level=logging.ERROR) # Error level
raise EmailAlreadyExists(log_level=None) # No log
```

#### Ce qu'il manque

- Gestion des erreurs multiples (renvoyer plusieurs erreurs dans un seul endpoint). Cela peut être utile pour les gros formulaires par exemple.
