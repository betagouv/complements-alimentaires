<template>
  <div class="fr-container pb-6">
    <DsfrBreadcrumb class="mb-8" :links="[{ to: '/', text: 'Accueil' }, { text: `Recherche : « ${searchTerm} »` }]" />
    <h1 class="fr-h3">Résultats de recherche</h1>
    {{ searchTerm }}
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { useRoute, onBeforeRouteUpdate } from "vue-router"

const route = useRoute()
const searchTerm = ref(null)

onBeforeRouteUpdate((to) => {
  if (!to.query?.q) return false
})
onMounted(() => {
  searchTerm.value = route.query.q
})
</script>
