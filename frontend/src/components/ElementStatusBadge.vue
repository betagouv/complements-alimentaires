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
]
</script>
