<template>
  <DsfrHeader :logo-text="logoText" service-title="Compléments alimentaires" />
  <router-view></router-view>
  <DsfrFooter :logo-text="logoText">
    <template v-slot:description>
      <p>Compléments alimentaires</p>
    </template>
  </DsfrFooter>
</template>

<script setup>
const logoText = ["Ministère", "de l'Agriculture", "et de la Souveraineté", "Alimentaire"]
</script>
