<template>
  <div>
    <DsfrInput
      label="Ajouter une synonyme (facultatif)"
      label-visible
      :hint="requestName ? `Concernant la demande « ${requestName} »` : ''"
      class="mb-2"
      @update:modelValue="updateNewSynonym"
    />
    <div v-if="initialSynonyms && initialSynonyms.length" class="mt-4">
      <p class="mb-1">Les synonymes existants :</p>
      <ul>
        <li v-for="s in initialSynonyms" :key="s.id">{{ s.name }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
// TODO: rename file to be just ReplacementModal or something?
import { ref, computed } from "vue"
import { getElementName } from "@/utils/elements"

const props = defineProps({ initialSynonyms: Array, requestElement: Object })
const requestName = computed(() => getElementName(props.requestElement))

const synonyms = defineModel()

const updateNewSynonym = (value) => {
  const lastIdx = synonyms.value.length - 1
  if (synonyms.value[lastIdx].id) {
    synonyms.value.push({ name: value })
  } else {
    synonyms.value.splice(lastIdx, 1, { name: value })
  }
}
</script>
