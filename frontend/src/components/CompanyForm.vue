<template>
  <div>
    <FormWrapper class="mx-auto">
      <DsfrFieldset legend="Informations administratives de l'entreprise">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'socialName')">
          <DsfrInput v-model="state.socialName" label="Dénomination sociale" required labelVisible />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'commercialName')">
          <DsfrInput v-model="state.commercialName" label="Nom commercial" required labelVisible />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'address')">
          <DsfrInput v-model="state.address" label="Adresse" required labelVisible hint="Numéro et voie" />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'additionalDetails')">
          <DsfrInput
            v-model="state.additionalDetails"
            label="Complément d’adresse (optionnel)"
            labelVisible
            hint="Bâtiment, immeuble, escalier et numéro d’appartement"
          />
        </DsfrInputGroup>
        <div class="md:flex md:gap-x-4 -my-4">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'postalCode')">
            <DsfrInput v-model="state.postalCode" label="Code postal" required labelVisible />
          </DsfrInputGroup>
          <div class="grow">
            <DsfrInputGroup :error-message="firstErrorMsg(v$, 'city')">
              <DsfrInput v-model="state.city" label="Ville" required labelVisible />
            </DsfrInputGroup>
          </div>
        </div>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'cedex')">
          <DsfrInput v-model="state.cedex" label="Cedex (optionnel)" labelVisible />
        </DsfrInputGroup>
      </DsfrFieldset>

      <DsfrCheckboxSet
        class="max-w-3xl"
        v-model="state.activities"
        :options="allActivities"
        :error-message="firstErrorMsg(v$, 'activities')"
      >
        <template #legend>
          Activités de l'entreprise
          <span class="fr-hint-text">
            Veuillez cocher obligatoirement une ou plusieurs des six cases proposées correspondant au type d’activité
            exercée par le déclarant.
          </span>
        </template>
      </DsfrCheckboxSet>
      <DsfrFieldset
        legend="Informations de contact"
        hint="Veuillez transmettre les coordonnées d’une personne au sein de la société que la DGAL pourra être amenée à contacter en cas de nécessité ou pour des informations complémentaires."
      >
        <div class="grid gap-x-4 grid-cols-1 md:grid-cols-2 -my-4">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'phoneNumber')">
            <DsfrInput
              required
              type="tel"
              v-model="state.phoneNumber"
              label="N° de téléphone de contact"
              labelVisible
            />
          </DsfrInputGroup>
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'email')">
            <DsfrInput required v-model="state.email" label="Adresse e-mail de contact" labelVisible />
          </DsfrInputGroup>
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'website')">
            <DsfrInput v-model="state.website" label="Site web de l'entreprise (optionnel)" labelVisible />
          </DsfrInputGroup>
        </div>
      </DsfrFieldset>
      <div class="flex gap-x-2 mt-8">
        <DsfrButton v-if="showCancelButton" @click="$emit('editCancelled')" secondary>
          Annuler
          <span class="fr-sr-only">la modification de l'entreprise</span>
        </DsfrButton>
        <DsfrButton label="Enregistrer l'entreprise" @click="submitCompany" :disabled="isFetching" />
      </div>
    </FormWrapper>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useVuelidate } from "@vuelidate/core"
import FormWrapper from "@/components/FormWrapper"
import { firstErrorMsg } from "@/utils/forms"
import { allActivities } from "@/utils/mappings"
import { errorRequiredField, errorRequiredEmail } from "@/utils/forms"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"
import { useFetch } from "@vueuse/core"

// Props & emits
const props = defineProps({ initialState: Object, url: String, method: String, showCancelButton: Boolean })
const emit = defineEmits(["responseReady", "editCancelled"])

// Shallow copie de la prop pour pouvoir modifier le state localement sans affecter le parent
// cf. https://vuejs.org/guide/components/props.html#mutating-object-array-props
const state = ref({ ...props.initialState })

const rules = {
  socialName: errorRequiredField,
  commercialName: errorRequiredField,
  address: errorRequiredField,
  additionalDetails: {},
  postalCode: errorRequiredField,
  city: errorRequiredField,
  cedex: {},
  // `country` et `siret/vat` ne sont pas affichés dans le formulaire car déjà entrés plus tôt
  activities: errorRequiredField,
  phoneNumber: errorRequiredField,
  email: errorRequiredEmail,
  website: {},
}

const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

// Définition et exécution de la requête
const { data, response, execute, isFetching } = useFetch(
  props.url,
  {
    headers: headers(),
  },
  { immediate: false }
)
  [props.method](state)
  .json()

const submitCompany = async () => {
  v$.value.$clearExternalResults()
  v$.value.$validate()
  if (v$.value.$error) {
    return
  }
  await execute()
  $externalResults.value = await handleError(response)
  emit("responseReady", data) // prévient le composant parent que la réponse est prête et lui retourne les données
}
</script>
