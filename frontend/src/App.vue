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
import AppHeader from "@/components/AppHeader.vue"
</script>
