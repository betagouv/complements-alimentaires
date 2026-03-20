<template>
  <div class="border p-4 bg-gray-50 text-right relative">
    <slot name="content"></slot>
    <ul class="list-none pl-0 my-0" role="list">
      <li v-if="selectedTabIndex > 0" class="inline">
        <DsfrButton secondary @click="emit('back')">
          <span v-if="props.removeSaveLabel">Revenir</span>
          <span v-else>
            Sauvegarder
            <span class="fr-sr-only">« {{ currentTabTitle }} »</span>
            et revenir
          </span>
          à l'onglet « {{ previousTabTitle }} »
        </DsfrButton>
      </li>
      <li v-if="selectedTabIndex < titles.length - 1" class="ml-4 inline">
        <DsfrButton @click="emit('forward')">
          <span v-if="props.removeSaveLabel">Passer</span>
          <span v-else>
            Sauvegarder
            <span class="fr-sr-only">« {{ currentTabTitle }} »</span>
            et passer
          </span>
          à l'onglet « {{ nextTabTitle }} »
        </DsfrButton>
      </li>
    </ul>
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
