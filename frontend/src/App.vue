<template>
  <router-view></router-view>
  <AppToaster :messages="messages" @close-message="removeMessage($event)" />
</template>

<script setup>
import { watch } from "vue"
import { useRoute } from "vue-router"
import AppToaster from "@/components/AppToaster.vue"
import useToaster from "@/composables/use-toaster"

const route = useRoute()
const { messages, removeMessage } = useToaster()

watch(route, (to) => {
  const suffix = "Compl'Alim"
  document.title = to.meta.title ? to.meta.title + " - " + suffix : suffix
})
</script>

<style>
.fr-pagination__list {
  @apply justify-center;
}
</style>
