<template>
  <div class="fr-container pb-10">
    <DsfrBreadcrumb :links="[{ to: '/', text: 'Accueil' }, { text: 'Plan du site' }]" />
    <h1>Plan du site</h1>
    <ul>
      <li v-for="page in pages" :key="page.path">
        <router-link :to="{ name: page.name }">{{ page.meta?.title || page.path }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { routes } from "@/router/index.js"

const pages = computed(() => {
  return routes.filter((route) => route.meta?.sitemap)
})
</script>
