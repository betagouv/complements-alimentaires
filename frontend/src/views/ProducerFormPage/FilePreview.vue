<template>
  <div class="border p-4 flex flex-col gap-2">
    <div class="border-b -mx-4 -mt-4 h-32 bg-blue-france-975 flex justify-center items-center">
      <v-icon v-if="isPDF" scale="3" name="ri-file-text-line" />
      <img v-else :src="file.file" class="object-contain h-32" :alt="`Image téléchargée ${props.file.name}`" />
    </div>
    <div class="fr-text--sm grow !mb-0">{{ props.file.name }}</div>
    <DsfrInputGroup class="max-w-sm" v-if="!hideTypeSelection">
      <DsfrSelect
        label="Type de document"
        defaultUnselectedText=""
        v-model="file.type"
        :options="documentTypes"
        :required="true"
      />
    </DsfrInputGroup>
    <div>
      <DsfrButton @click="$emit('remove', file)" label="Supprimer" secondary size="sm" />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({ file: Object, hideTypeSelection: Boolean })
const isPDF = computed(() => props.file.name.endsWith("pdf"))

// TODO: À voir si on peut le mettre dans la base de données aussi
const documentTypes = [
  "Attestation d'une autorité compétente",
  "Compléments info professionnel",
  "Observations professionnel",
  "Autre courrier du professionnel",
  "Brouillon",
  "Autre professionnel",
  "Preuve règlementaire",
  "Bulletin d'analyse",
]
</script>
