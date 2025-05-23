<template>
  <div class="mt-1 fr-hint-text flex flex-col">
    <DsfrBadge
      v-for="rule in passwordRules"
      :key="rule"
      :label="rule"
      class="block! lowercase! bg-transparent! pl-0!"
      small
      type="info"
    />
  </div>
</template>

<script setup>
const passwordRules = [
  "doit contenir au minimum 8 caractères",
  "ne peut pas être entièrement numérique",
  "ne peut pas trop ressembler à vos autres informations personnelles",
]
</script>
