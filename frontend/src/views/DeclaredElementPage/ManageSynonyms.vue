<template>
  <div>
    <DsfrInput
      label="Ajouter une synonyme (optionnelle)"
      label-visible
      :hint="requestName ? `Le nom de la demande : ${requestName}` : ''"
      v-model="newSynonym"
      class="mb-2"
    />
    <div v-if="synonyms && synonyms.length" class="mt-4">
      <p class="mb-1">Les synonymes existantes :</p>
      <ul>
        <li v-for="s in synonyms" :key="s.id">{{ s.name }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
// TODO: rename file to be just ReplacementModal or something?
import { onMounted, ref, computed } from "vue"
import { getElementName } from "@/utils/elements"

// TODO: define model instead
const props = defineProps({ initialSynonyms: Array, requestElement: Object })
const synonyms = ref()

// TODO: check this still works if select, open, cancel, reselect, open
// or if edit, cancel and come back (should see original list)
onMounted(() => {
  synonyms.value = props.initialSynonyms
})

const requestName = computed(() => getElementName(props.requestElement))
</script>
