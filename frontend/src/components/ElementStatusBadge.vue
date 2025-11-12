<template>
  <!-- Nous n'utilisons pas le mot "autorisé" pour ne pas donner une fausse idée d'acceptation sure de l'ingrédient -->
  <DsfrBadge v-if="text === 'autorisé'" label="déclarable" small type="info" />
  <DsfrBadge v-else-if="text === 'non autorisé'" :label="text" small type="error" />
  <DsfrBadge v-else-if="text === 'retiré par l\'administration'" :label="text" small type="error" />
</template>

<script setup>
defineProps({
  text: String,
})
</script>
