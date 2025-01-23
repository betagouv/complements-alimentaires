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
import { computed } from "vue"
import { getElementName } from "@/utils/elements"

const props = defineProps({ initialSynonyms: Array, requestElement: Object })
const requestName = computed(() => getElementName(props.requestElement))

const synonyms = defineModel()

const updateNewSynonym = (value) => {
  const newSynonym = { name: value }

  const count = synonyms.value.length
  const lastIdx = count - 1
  const addSynonym = count && synonyms.value[lastIdx].id
  const updateSynonym = count && !addSynonym

  if (addSynonym) synonyms.value.push(newSynonym)
  else if (updateSynonym) synonyms.value.splice(lastIdx, 1, newSynonym)
  else synonyms.value = [newSynonym]
}
</script>
