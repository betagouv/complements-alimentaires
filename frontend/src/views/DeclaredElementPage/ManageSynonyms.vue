<template>
  <div>
    <h2>Synonymes</h2>
    <!-- TODO; what key to use given potential for deletion and adding multiple empty entries? -->
    <div v-for="(s, idx) in synonyms" :key="idx" class="flex items-center">
      <DsfrInput label="Synonyme" v-model="s.name" class="mb-2" />

      <DsfrButton
        :label="`Supprimer synonyme '${s.name}'`"
        icon="ri-delete-bin-6-line"
        icon-only
        tertiary
        no-outline
        @click="deleteSynonym(s)"
      />
    </div>
    <DsfrButton label="Ajouter synonyme" icon="ri-add-line" secondary @click="addSynonym" />
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue"

const props = defineProps({ initialSynonyms: Array })

const synonyms = ref()

// TODO: check this still works if select, open, cancel, reselect, open
onMounted(() => {
  synonyms.value = props.initialSynonyms
})

const addSynonym = () => {
  synonyms.value.push({})
}

const deleteSynonym = (synonym) => {}
</script>
