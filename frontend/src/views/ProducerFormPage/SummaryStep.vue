<template>
  <DsfrAlert v-if="!readonly">
    <p class="mb-2">Veuillez vérifier les données ci-dessous avant de procéder à la validation de votre démarche</p>
    <DsfrButton @click="emit('submit')" label="Soumettre ma démarche" />
  </DsfrAlert>

  <SectionTitle class="!mt-8" title="Votre démarche" sizeTag="h6" icon="ri-file-text-line" />
  <DeclarationSummary v-model="payload" :readonly="readonly" />
</template>

<script setup>
import DeclarationSummary from "@/components/DeclarationSummary"
import SectionTitle from "@/components/SectionTitle"

const payload = defineModel()
const emit = defineEmits(["submit"])
defineProps({ readonly: Boolean })
</script>
