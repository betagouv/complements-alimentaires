<template>
  <AppHeader />
  <router-view></router-view>
  <DsfrFooter :logo-text="logoText">
    <template v-slot:description>
      <p>Compléments alimentaires</p>
    </template>
  </DsfrFooter>
</template>

<script setup>
import { watch } from "vue"
import { useRoute } from "vue-router"
import AppHeader from "@/components/AppHeader.vue"

const route = useRoute()

watch(route, (to) => {
  const suffix = "Compléments alimentaires"
  document.title = to.meta.title ? to.meta.title + " - " + suffix : suffix
})
</script>
