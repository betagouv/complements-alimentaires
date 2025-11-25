<template>
  <div class="fr-container pb-10">
    <DsfrBreadcrumb :links="[{ to: '/', text: 'Accueil' }, { text: 'Mentions Légales' }]" />
    <h1>Mentions Légales</h1>
    <h2>Éditeur de la Plateforme</h2>
    <p>
      La Plateforme Compl'Alim (
      <router-link :to="{ name: 'LandingPage' }">https://compl-alim.beta.gouv.fr/</router-link>
      ) est éditée par l'Incubateur de services numériques de la Direction Interministérielle du Numérique (DINUM).
    </p>
    <h2>Coordonnées</h2>
    <p>Adresse : DINUM, 20 avenue de Ségur, 75007 Paris</p>
    <p>Tel. accueil : 01.71.21.01.70</p>
    <p>SIRET : 12000101100010 (secrétariat général du gouvernement)</p>
    <p>SIREN : 120 001 011</p>
    <h2>Directeur de la publication</h2>
    <address>
      <p>
        Ministère de l’Agriculture et de la Souveraineté Alimentaire
        <br />
        Direction Générale de l’Alimentation
        <br />
        Hôtel de Villeroy, 78, rue de Varenne; Paris 7e
      </p>
    </address>
    <h2>Hébergement de la Plateforme</h2>
    <p>Ce site est hébergé en propre par:</p>
    <address>
      <p>Clevercloud, 3 rue de l'Allier, 44000 Nantes, France.</p>
    </address>
    <h2>Accessibilité</h2>
    <p>
      La conformité aux normes d’accessibilité numérique est un objectif ultérieur dans le développement itératif de la
      plateforme. Nous nous efforçons de créer un maximum de composants partagés et de les rendre accessibles à toutes
      et tous.
    </p>
    <p>
      Pour en savoir plus :
      <a href="http://references.modernisation.gouv.fr/accessibilite-numerique" target="_blank" rel="noopener">
        http://references.modernisation.gouv.fr/accessibilite-numerique.
      </a>
    </p>
    <p>
      Pour nous signaler des problèmes ou suggestions d'amélioration concernant l'accessibilité de la plateforme, deux
      options :
    </p>
    <ul>
      <li>
        nous signaler par email :
        <a :href="'mailto:' + contact_email">{{ contact_email }}</a>
      </li>
      <li>
        créer une “issue” sur
        <a href="https://github.com/betagouv/complements-alimentaires/" target="_blank" rel="noopener">
          le dépôt de code sur GitHub.
        </a>
      </li>
    </ul>
    <p>
      Le code source est ouvert et les contributions sont bienvenues.
      <a href="https://github.com/betagouv/complements-alimentaires/" target="_blank" rel="noopener">
        Voir le code source.
      </a>
    </p>
    <h2>Données personnelles, suivi d’audience et gestion des cookies</h2>
    <p>
      Le cookie est un petit fichier texte enregistré par le navigateur de votre ordinateur, tablette ou smartphone et
      qui permet de conserver des données utilisateur afin de faciliter la navigation et de permettre certaines
      fonctionnalités.
    </p>
    <h3>A quoi nous servent-ils ?</h3>
    <p>Cela nous permet de mesurer le nombre de visites et de comprendre quelles sont les pages les plus consultées.</p>
    <h3>Ce site n’affiche pas de bannière de consentement aux cookies, pourquoi ?</h3>
    <p>
      C’est vrai, vous n’avez pas eu à cliquer sur un bloc qui recouvre la moitié de la page pour dire que vous êtes
      d’accord avec le dépôt de cookies — même si vous ne savez pas ce que ça veut dire !
    </p>
    <p>
      Rien d’exceptionnel, pas de passe-droit lié à un .gouv.fr. Nous respectons simplement la loi, qui dit que certains
      outils de suivi d’audience, correctement configurés pour respecter la vie privée, sont exemptés d’autorisation
      préalable.
    </p>
    <p>
      Nous utilisons pour cela
      <a href="https://matomo.org/" target="_blank" rel="noopener">Matomo</a>
      , un outil
      <a href="https://matomo.org/free-software/" target="_blank" rel="noopener">libre</a>
      , paramétré pour être en conformité avec la
      <a href="https://www.cnil.fr/fr/solutions-pour-la-mesure-daudience" target="_blank" rel="noopener">
        recommandation « Cookies »
      </a>
      de la CNIL. Cela signifie que votre adresse IP, par exemple, est anonymisée avant d’être enregistrée. Il est donc
      impossible d’associer vos visites sur ce site à votre personne.
    </p>
    <h3>Je contribue à enrichir vos données, puis-je y accéder ?</h3>
    <p>
      Bien sûr ! Les statistiques d’usage de la majorité de nos produits, dont
      <a href="https://beta.gouv.fr/" target="_blank" rel="noopener">beta.gouv.fr,</a>
      sont disponibles en accès libre sur
      <a
        href="https://stats.beta.gouv.fr/index.php?module=CoreHome&action=index&idSite=95&period=day&date=yesterday#?period=day&date=yesterday&category=Dashboard_Dashboard&subcategory=1"
      >
        stats.beta.gouv.fr.
      </a>
    </p>
  </div>
</template>
<script>
// eslint-disable-next-line no-unused-vars
const contact_email = window.CONTACT_EMAIL
</script>
