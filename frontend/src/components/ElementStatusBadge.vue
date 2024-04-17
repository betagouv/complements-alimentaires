<template>
  <DsfrBadge :label="text" small :type="badgeTypes.find((x) => x.text === text)?.type" />
</template>

<script setup>
defineProps({
  text: String,
})

const badgeTypes = [
  { text: "Autorisé", type: "success" },
  { text: "Non autorisé", type: "error" },
  { text: "À inscrire", type: "new" }, // TODO: trouver un wording plus user friendly et compréhensible
  { text: "Sans objet", type: "warning" }, // TODO: ne pas afficher ce statut lorsqu'il est présent
]
</script>
