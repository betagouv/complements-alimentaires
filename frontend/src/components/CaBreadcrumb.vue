<template>
  <nav role="navigation" class="fr-breadcrumb" :aria-label="navigationLabel">
    <div>
      <ol class="fr-breadcrumb__list">
        <li v-for="(link, index) in links" :key="index" class="fr-breadcrumb__item" data-testid="lis">
          <RouterLink
            v-if="link.to"
            class="fr-breadcrumb__link"
            :to="link.to"
            :aria-current="index === links.length - 1 ? 'page' : undefined"
          >
            {{ link.text }}
          </RouterLink>
          <a
            v-if="!link.to"
            class="fr-breadcrumb__link"
            :aria-current="index === links.length - 1 ? 'page' : undefined"
          >
            {{ link.text }}
          </a>
        </li>
      </ol>
    </div>
  </nav>
</template>

<script setup>
// Ce composant existe car Tanaguru invalide le critère 7.1 pour le fil d'Ariane comme définit par le DSFR
// La non-conformité est sur le bouton avec aria-expanded qui disparaît après être cliqué.
// Il y a plusieurs options :
// 1. garder le bouton disclosure visible tout le temps
// 2. enlever le aria-expanded du bouton
// 3. laisser le fil d'Ariane visible tout le temps
// 1 et 2 demande plus de travail sur la fonctionnement et design du composant
// 3 est le plus facile et n'est pas très mal pour un site qui n'a pas beaucoup de profondeur de navigation
//   alors les liens toujours affichés ne prennent pas plus d'espace verticale que le bouton originel

const props = defineProps({
  links: { type: Array, default: () => [{ text: "" }] },
  navigationLabel: { type: String, default: "vous êtes ici :" },
})
</script>
