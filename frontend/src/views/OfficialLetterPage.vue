<template>
  <div>
    <p>Cher {{ name }},</p>
    <p>Ceci est une lettre officielle de l'état.</p>
    <p>Elle n'utilise volontairement pas de layout, et n'a donc aucun margin.</p>
    <p>
      Plus tard, l'url qui affiche cette page sera utilisée par une view Django pour générer un PDF à partir d'elle (et
      c'est le PDF lui-même qui créera les marges).
    </p>
  </div>
</template>

<script setup>
defineProps({ name: { type: String, required: true } })
</script>

<style scoped></style>
