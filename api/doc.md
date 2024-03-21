# Documentation sur l'API

### Gestion personnalisée des erreurs

#### Pourquoi ?

- Avoir un format de retour d'erreur toujours identique, peu importe l'erreur qui survient (prédictivité)
- Avoir un format de retour d'erreur qui contient les infos nécessaires et suffisantes pour savoir comment les afficher côté front (ex : dans un toast, dans un formulaire, etc.)
- Pouvoir gérer nos erreurs d'API sous forme d'exceptions personnalisées, et les lever facilement dans nos endpoinds
- Écrire un log
- Le tout automatiquement, sans avoir à gérer cela manuellement à chaque fois.

#### Fonctionnement des erreurs avec DRF

- DRF dispose d'un mécanisme natif de gestion d'exceptions sur lequel nous nous appuyons pour ne pas réinventer la roue. Il dispose de la classe `APIException` dont hérite de nombreuses erreurs standards comme par exemple `MethodNotAllowed` ou `AuthenticationFailed`.
- Aussi, lorsque la validation se fait du côté des serializers, une `ValidationError` (de type `APIException` aussi) peut être levée.
- DRF propose d'utilise un custom handler : une fonction qui sera appelée dès qu'une exception est levée dans un endpoint, pour nous permettre de personnaliser la réponse à ce moment.

#### Ce qu'on ajoute

- Nous créeons une classe d'exception `ProjectAPIException` qui permet de formatter une réponse toujours de la même manière.


- Dans le custom handler, en fonction du type de cas rencontré, nous nous assurons de récupérer les données initiales, puis de les réinjecter dans `ProjectAPIException` pour avoir un formattage identique. Nous gérons aussi à ce moment le code HTTP renvoyé

- Le format que nous avons choisi permet de distinguer 3 types d'erreurs utilisables différemment dans notre front-end. Voici un exemple de réponse qui contiendrait les 3 :

```py
{
    "global_error": "msg", # à afficher dans un toast
    "non_field_errors": ["msg", "msg"], # en haut d'un formulaire
    "field_errors": {"field_1": ["msg", "msg"], "field_2": ["msg"]} # dans les champs d'un formulaire
}
```

À noter que la classe ProjectAPIException, en plus de servir au formattage des erreurs par DRF, peut être surclassée pour créer nos propres exceptions, utilisables directement dans un endpoint Django. Par exemple :

```python
class EmailAlreadyExists(ProjectAPIException):
    field_errors = {"email" : "L'adresse e-mail renseignée existe déjà."}
```

```python
class SomeEndpoint(APIView):
    raise EmailAlreadyExists
```

Évidemment, si l'exception n'a pas vocation à être réutilisée, elle peut être levée directement dans le endpoint :

```python
class SomeEndpoint(APIView):
    raise ProjectAPIException(global_error="Une erreur qui ne peut se produire que dans ce endpoint.")
```

- Chaque ProjectAPIException écrit un log de level "INFO" par défaut. Cela peut être changé. Par exemple :

```python
raise EmailAlreadyExists(log_level=logging.ERROR) # Log de niveau ERROR
raise EmailAlreadyExists(log_level=None) # Pas de log écrit
```
