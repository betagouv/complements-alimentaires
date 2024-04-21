<template>
  <DsfrBadge :label="text" small :type="badgeTypes.find((x) => x.text === text)?.type" />
</template>

<script setup>
defineProps({
  text: String,
})

const badgeTypes = [
  { text: "autorisé", type: "success" },
  { text: "non autorisé", type: "error" },
  { text: "à inscrire", type: "new" }, // TODO: trouver un wording plus user friendly et compréhensible
  { text: "sans objet", type: "warning" }, // TODO: ne pas afficher ce statut lorsqu'il est présent
]
</script>
