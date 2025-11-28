<template>
  <!-- Nous n'utilisons pas le mot "autorisé" pour ne pas donner une fausse idée d'acceptation sure de l'ingrédient -->
  <DsfrBadge v-if="text === ingredientStatuses.AUTHORIZED.apiValue" label="déclarable" small type="info" />
  <DsfrBadge v-else-if="text === ingredientStatuses.NOT_AUTHORIZED.apiValue" :label="text" small type="error" />
  <DsfrBadge v-else-if="text === ingredientStatuses.AUTHORIZATION_REVOKED.apiValue" :label="text" small type="error" />
</template>

<script setup>
import { ingredientStatuses } from "@/utils/mappings"

defineProps({
  text: String,
})
</script>
