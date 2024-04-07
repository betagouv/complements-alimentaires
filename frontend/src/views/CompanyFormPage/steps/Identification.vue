<template>
  <div>
    <FormWrapper class="max-w-xl mx-auto">
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'country')">
        <CountryField v-model="state.country" description="Dans quel pays l'entreprise est-elle immatriculée ?" />
      </DsfrInputGroup>
      <template v-if="state.country === 'FR'">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'siret')">
          <DsfrInput v-model="state.siret" label="Numéro de SIRET" required labelVisible @input="removeSpaces" />
          <div class="mt-2">
            <a class="fr-link" target="_blank" rel="noopener" href="https://annuaire-entreprises.data.gouv.fr/">
              Annuaire des entreprises
            </a>
          </div>
        </DsfrInputGroup>
        <DsfrButton @click="nextStep" v-if="step == 0" label="Démarrer !" size="lg" />
        <DsfrButton label="Vérifier le SIRET" icon="ri-arrow-right-line" iconRight @click="validateSiret" />
      </template>

      <template v-if="state.country && state.country !== 'FR'">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'vatIdNumber')">
          <DsfrInput v-model="state.vatIdNumber" label="Numéro de TVA intracommunautaire" required labelVisible />
        </DsfrInputGroup>
        <DsfrButton label="Vérifier le n° de TVA" icon="ri-arrow-right-line" iconRight />
      </template>
    </FormWrapper>
  </div>
</template>

<script setup>
import { ref } from "vue"
import FormWrapper from "@/components/FormWrapper"
import CountryField from "@/components/fields/CountryField"
import { errorRequiredField, firstErrorMsg } from "@/utils/forms"
import { useVuelidate } from "@vuelidate/core"

// Form state & rules
const state = ref({
  country: undefined,
  siret: "",
  vatIdNumber: "",
})

const rules = {
  country: errorRequiredField,
  siret: errorRequiredField,
  vatIdNumber: errorRequiredField,
}

const v$ = useVuelidate(rules, state)

// todo: replace by result from backend
const emit = defineEmits(["unexist", "exist"])

const validateSiret = () => {
  if (state.value.siret == "A") emit("exist")
  if (state.value.siret == "B") emit("unexist")
}

const removeSpaces = (event) => (event.target.value = event.target.value.replace(/\s/g, ""))
</script>
