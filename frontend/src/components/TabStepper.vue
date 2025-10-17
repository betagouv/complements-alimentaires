<template>
  <div class="border p-4 bg-gray-50 text-right relative">
    <slot name="content"></slot>
    <DsfrButton secondary v-if="selectedTabIndex > 0" @click="emit('back')" :label="backLabel" />
    <DsfrButton class="ml-4" v-if="selectedTabIndex < titles.length - 1" @click="emit('forward')" :label="fwdLabel" />
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps(["titles", "selectedTabIndex", "removeSaveLabel"])
const emit = defineEmits(["back", "forward"])

const backLabel = computed(() => {
  if (props.removeSaveLabel) return `Revenir à l'onglet « ${props.titles[props.selectedTabIndex - 1].title} »`
  return `Sauvegarder et revenir à l'onglet « ${props.titles[props.selectedTabIndex - 1].title} »`
})

const fwdLabel = computed(() => {
  if (props.removeSaveLabel) return `Passer à l'onglet « ${props.titles[props.selectedTabIndex + 1].title} »`
  return `Sauvegarder et passer à l'onglet « ${props.titles[props.selectedTabIndex + 1].title} »`
})
</script>
