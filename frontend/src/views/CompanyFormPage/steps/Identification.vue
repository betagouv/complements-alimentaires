<template>
  <div>
    <FormWrapper class="max-w-xl mx-auto">
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'country')">
        <DsfrSelect
          defaultUnselectedText="Choisissez un pays"
          :options="countryChoices"
          v-model="state.country"
          label="Pays"
          description="Dans quel pays l'entreprise est-elle immatriculée ?"
          required
          labelVisible
        />
      </DsfrInputGroup>
      <template v-if="state.country === 'FR'">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'siret')">
          <DsfrInput v-model="state.siret" label="Numéro de SIRET" required labelVisible />
          <div class="mt-2">
            <a class="fr-link" target="_blank" rel="noopener" href="https://annuaire-entreprises.data.gouv.fr/">
              Annuaire des entreprises
            </a>
          </div>
        </DsfrInputGroup>
        <DsfrButton
          label="Vérifier le SIRET (existe en base)"
          icon="ri-arrow-right-line"
          iconRight
          @click="validateSiretExist"
        />
        <DsfrButton
          label="Vérifier le SIRET (n'existe pas)"
          icon="ri-arrow-right-line"
          iconRight
          @click="validateSiretUnexist"
        />
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
import { ref, onMounted } from "vue"
import { useFetch } from "@vueuse/core"
import { useVuelidate } from "@vuelidate/core"
import FormWrapper from "@/components/FormWrapper"
import { handleError } from "@/utils/error-handling"
import { errorRequiredField, firstErrorMsg } from "@/utils/forms"

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

// Initial request for gettings countries (TODO: isolate in a component?)
const {
  data: countryChoices,
  response: countryResponse,
  execute: executeGetCountries,
} = useFetch("/api/v1/countries/", { immediate: false }).json()

onMounted(async () => {
  await executeGetCountries()
  await handleError(countryResponse)
})

// todo: replace by result from backend
const emit = defineEmits(["unexist", "exist"])

const validateSiretExist = () => {
  emit("exist")
}

const validateSiretUnexist = () => {
  emit("unexist")
}
</script>
