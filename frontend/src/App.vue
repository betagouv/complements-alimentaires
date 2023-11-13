<template>
  <DsfrHeader :logo-text="logoText" service-title="Compléments alimentaires" />
  <div class="p-6">
    <h1>Compléments alimentaires</h1>
    <p>En construction</p>
  </div>
  <DsfrFooter :logo-text="logoText">
    <template v-slot:description>
      <p>Compléments alimentaires</p>
    </template>
  </DsfrFooter>
</template>

<script setup>
const logoText = [
  "Ministère",
  "de l'Agriculture",
  "et de la Souveraineté",
  "Alimentaire",
];
</script>

<style scoped>
.fr-container {
  margin-top: 3rem;
  margin-bottom: 3rem;
}
</style>
