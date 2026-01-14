<template>
  <div class="border p-4 bg-gray-50 text-right relative">
    <slot name="content"></slot>
    <DsfrButton secondary v-if="selectedTabIndex > 0" @click="emit('back')">
      <span v-if="props.removeSaveLabel">Revenir</span>
      <span v-else>
        Sauvegarder
        <span class="fr-sr-only">« {{ currentTabTitle }} »</span>
        et revenir
      </span>
      à l'onglet « {{ previousTabTitle }} »
    </DsfrButton>
    <DsfrButton class="ml-4" v-if="selectedTabIndex < titles.length - 1" @click="emit('forward')">
      <span v-if="props.removeSaveLabel">Passer</span>
      <span v-else>
        Sauvegarder
        <span class="fr-sr-only">« {{ currentTabTitle }} »</span>
        et passer
      </span>
      à l'onglet « {{ nextTabTitle }} »
    </DsfrButton>
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps(["titles", "selectedTabIndex", "removeSaveLabel"])
const emit = defineEmits(["back", "forward"])

const previousTabTitle = computed(() => props.titles[props.selectedTabIndex - 1].title)
const currentTabTitle = computed(() => props.titles[props.selectedTabIndex].title)
const nextTabTitle = computed(() => props.titles[props.selectedTabIndex + 1].title)
</script>
