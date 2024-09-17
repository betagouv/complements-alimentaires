<template>
  <div>
    <SectionTitle title="Votre démarche" sizeTag="h6" icon="ri-file-text-line" />
    <DeclarationSummary v-model="payload" :readonly="readonly" />
    <hr />
    <h2>Soumettre</h2>
    <DsfrAlert v-if="!readonly">
      <DsfrInputGroup>
        <DsfrInput
          class="!max-w-lg"
          label="Commentaires à destination de l'administration"
          labelVisible
          v-model="comment"
          :isTextarea="true"
        />
      </DsfrInputGroup>
      <DsfrButton @click="emit('submit', comment)" label="Soumettre ma démarche" />
    </DsfrAlert>
  </div>
</template>

<script setup>
import { ref } from "vue"
import DeclarationSummary from "@/components/DeclarationSummary"
import SectionTitle from "@/components/SectionTitle"

const payload = defineModel()
const emit = defineEmits(["submit"])
const comment = ref("")
defineProps({ readonly: Boolean })
</script>
