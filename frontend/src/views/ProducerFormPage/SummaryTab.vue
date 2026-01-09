<template>
  <div>
    <div class="text-right">
      <a :href="`/declarations/${payload.id}/summary`" download class="text-sm font-medium">
        <v-icon name="ri-printer-line"></v-icon>
        Imprimer
      </a>
    </div>
    <SectionTitle title="Votre démarche" sizeTag="h6" icon="ri-file-text-line" />
    <DeclarationSummary v-model="payload" :readonly="readonly" />
    <hr v-if="!readonly" />
    <h2 v-if="!readonly">Soumettre</h2>
    <DsfrAlert v-if="!readonly">
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'comment')">
        <DsfrInput
          class="max-w-lg!"
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
            <router-link
              :to="{ name: 'CompliancePage' }"
              target="_blank"
              title="Informations supplémentaires sur la conformité au droit alimentaire - nouvelle fenêtre"
            >
              Informations supplémentaires sur la conformité au droit alimentaire.
            </router-link>
          </template>
        </DsfrCheckbox>
      </DsfrInputGroup>
      <DsfrButton :disabled="!conformityEngaged" @click="submitDeclaration">
        Soumettre ma démarche
        <span class="fr-sr-only">pour le produit « {{ payload.name }} »</span>
      </DsfrButton>
    </DsfrAlert>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import DeclarationSummary from "@/components/DeclarationSummary"
import SectionTitle from "@/components/SectionTitle"
import { useVuelidate } from "@vuelidate/core"
import { errorRequiredField, firstErrorMsg } from "@/utils/forms"

const conformityEngaged = ref(false)

const payload = defineModel()
const emit = defineEmits(["submit"])
const comment = ref("")

const rules = computed(() => {
  if (payload.value.status === "DRAFT") return {}
  return { comment: errorRequiredField }
})
const $externalResults = ref({})
const v$ = useVuelidate(rules, { comment }, { $externalResults })

const submitDeclaration = () => {
  v$.value.$reset()
  v$.value.$validate()
  if (!v$.value.$error) emit("submit", comment.value)
}

defineProps({ readonly: Boolean })
</script>
