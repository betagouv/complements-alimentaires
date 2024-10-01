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
      <hr />
      <DsfrInputGroup>
        <DsfrCheckbox v-model="conformityEngaged">
          <template v-slot:label>
            <span>
              J'atteste que ce produit répond aux prescriptions du droit alimentaire qui lui sont applicables.
            </span>
            <router-link :to="{ name: 'CompliancePage' }" target="_blank">
              Informations supplémentaires sur la conformité au droit alimentaire.
            </router-link>
          </template>
        </DsfrCheckbox>
      </DsfrInputGroup>
      <DsfrButton :disabled="!conformityEngaged" @click="emit('submit', comment)" label="Soumettre ma démarche" />
    </DsfrAlert>
  </div>
</template>

<script setup>
import { ref } from "vue"
import DeclarationSummary from "@/components/DeclarationSummary"
import SectionTitle from "@/components/SectionTitle"

const conformityEngaged = ref(false)

const payload = defineModel()
const emit = defineEmits(["submit"])
const comment = ref("")
defineProps({ readonly: Boolean })
</script>
