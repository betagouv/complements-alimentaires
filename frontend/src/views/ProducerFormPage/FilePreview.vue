<template>
  <div class="border p-4 flex flex-col gap-2">
    <div class="border-b -mx-4 -mt-4 h-32 bg-blue-france-975 flex justify-center items-center">
      <v-icon v-if="isPDF" scale="3" name="ri-file-text-line" />
      <img v-else :src="file.file" class="object-contain h-32" :alt="`Image téléchargée ${props.file.name}`" />
    </div>
    <div class="fr-text--sm grow !mb-0">{{ props.file.name }}</div>
    <DsfrInputGroup class="max-w-sm" v-if="!hideTypeSelection && !props.readonly">
      <DsfrSelect
        label="Type de document"
        defaultUnselectedText=""
        v-model="file.type"
        :options="documentTypes"
        :required="true"
      />
    </DsfrInputGroup>
    <div v-else>{{ documentTypes.find((x) => x.value === file.type)?.text }}</div>
    <div v-if="!props.readonly">
      <DsfrButton @click="$emit('remove', file)" label="Supprimer" secondary size="sm" />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({ file: Object, hideTypeSelection: Boolean, readonly: Boolean })
const isPDF = computed(() => props.file.name.endsWith("pdf"))

// TODO: Une fois qu'on aura confirmé les types de document, on peut les exposer via l'API pour ne pas
// les avoir hard-codés ici
const documentTypes = [
  { value: "LABEL", text: "Étiquetage" },
  { value: "REGULATORY_PROOF", text: "Preuve règlementaire" },
  { value: "CERTIFICATE_AUTHORITY", text: "Attestation d'une autorité compétente" },
  { value: "ADDITIONAL_INFO", text: "Compléments info professionnel" },
  { value: "OBSERVATIONS", text: "Observations professionnel" },
  { value: "PROFESSIONAL_MAIL", text: "Autre courrier du professionnel" },
  { value: "DRAFT", text: "Brouillon" },
  { value: "OTHER", text: "Autre professionnel" },
  { value: "ANALYSIS_REPORT", text: "Bulletin d'analyse" },
]
</script>
