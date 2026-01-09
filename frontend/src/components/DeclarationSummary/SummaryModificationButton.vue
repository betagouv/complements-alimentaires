<template>
  <router-link :to="to" class="fr-btn fr-btn--secondary fr-btn--sm">
    <span class="fr-sr-only">Retour à l'onglet {{ tabName }} pour</span>
    Modifier
    <span v-if="suffix" class="fr-sr-only">{{ suffix }}</span>
  </router-link>
</template>

<script setup>
defineProps(["to", "tabName", "suffix"])
</script>
