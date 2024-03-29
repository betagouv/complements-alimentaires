# Front-end

## Typescript ?

Par simplicité, le projet a été démarré en ES6, et ne permet pour le moment pas d'utiliser la syntaxe TS.
A terme, nous envisageons une migration progressive.

## Préférences ES6

Pour garder une certaine uniformité de la codebase, nous avons défini des préférences par défaut sur la syntaxe à utiliser, en particulier sur le langage ES6 qui est relativement permissif.

Ce ne sont que des préférences, et il est bien-sûr possible d'aller contre quand le contexte le justifie.

#### Asynchronisme

- Syntaxe préférée : `await`/`async`
- Raisons : généralement plus simple à écrire et lire

#### Fonctions

Les arrow functions n'étant pas iso-fonctionnelles avec `function`, on s'autorise à faire cohabiter les deux.

#### Strings

- Utilisation de strings "classiques" par défaut
- Utilisation de [template literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals) quand cela simplifie. Exemples :
    - collision entre une apostrophe d'un texte en français et des simple quotes
    - nombreuses variables à injecter (plus lisible qu'une concaténation avec `+`)

## Préférences Vue.js

#### Conventions officielles

- [Vue JS conventions officielles](https://vuejs.org/style-guide/)


#### Arborescence

- On nomme `<Feature>Page` tout composant défini comme route dans le router. Il peut s'agir :
    - du composant lui-même (ex: `BlogHomePage.vue`)
    - du dossier quand la page s'appelle `index.vue` (ex: `LandingPage`)
- Un composant local (lié à 1 page spécifique) se situe dans le dossier contenant cette page
- Un composant utilisé par plusieurs pages se situe dans le dossier `src/components/`


#### Data fetching

- Utilisation du composable [`useFetch`](https://vueuse.org/core/useFetch/)
- Raisons :
    - syntaxe déclarative plus simple
    - permet de récupérer depuis le composable des informations nécessaires sur la requête (ex: est-elle en cours ?)


## Composants d'UI

- Suivi des règles du DSFR
- Utilisation au maximum des composants disponibles dans la UI lib [vue-dsfr](https://vue-dsfr.netlify.app/)
- Lorsque les components Vue ne sont pas adaptés au besoin, nous pouvons aussi utiliser les classes CSS fournies par le DSFR.
- Si un comportement n'est pas disponible (ex : toaster, autocomplete, etc.) :
    1. Essayer de voir les différentes [recettes de la communauté](https://www.vue-ds.fr/recettes/) pour gagner du temps
    2. Arbitrer entre le fait de faire soi-même (chronophage ?) VS intégrer une autre librairie (lourd ?)

## CSS

- Utilisation de TailwindCSS quand c'est possible, CSS pur autrement.

## Code Linting & Formatting

- Utilisation de ESLint et Prettier
