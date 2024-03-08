<template>
  <div class="border p-4 flex flex-col gap-2">
    <div class="-mx-4 -mt-4 h-32 bg-slate-200 flex justify-center items-center">
      <v-icon v-if="isPDF" scale="3" name="ri-file-text-line" />
      <img v-else :src="file.file" class="object-contain h-32" :alt="`Image téléchargée ${props.file.name}`" />
    </div>
    <div class="fr-text--sm grow !mb-0">{{ props.file.name }}</div>
    <div>
      <DsfrButton @click="$emit('remove', file)" label="Supprimer" secondary size="sm" />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({ file: Object, showTypeSelection: Boolean })
const isPDF = computed(() => props.file.name.endsWith("pdf"))
</script>
