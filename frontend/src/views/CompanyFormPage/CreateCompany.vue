<template>
  <div>
    <DsfrAlert size="sm">
      L'entreprise dont le n°
      {{ company.identifierType.toUpperCase() + " " }}
      est
      <strong>{{ company.identifier }}</strong>
      n'est pas encore enregistrée dans notre base de données. Pour ce faire, veuillez vérifier ou compléter les
      informations ci-dessous. À l'issue, vous en deviendrez automatiquement son gestionnaire.
    </DsfrAlert>
    <FormWrapper class="mx-auto mt-8">
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
        <div class="block md:flex md:gap-x-4">
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

      <DsfrFieldset
        legend="Activités de l'entreprise"
        hint="Veuillez cocher obligatoirement une ou plusieurs des six cases proposées correspondant au
type d’activité exercée par le déclarant."
      >
        <DsfrCheckboxSet
          class="max-w-3xl"
          v-model="state.activities"
          :options="allActivities"
          :error-message="firstErrorMsg(v$, 'activities')"
        />
      </DsfrFieldset>
      <DsfrFieldset
        legend="Informations de contact"
        hint="Veuillez transmettre les coordonnées d’une personne au sein de la société que la DGAL pourra être amenée à contacter en cas de nécessité ou pour des informations complémentaires."
      >
        <div class="grid gap-4 grid-cols-1 md:grid-cols-2">
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
      <DsfrButton label="Enregistrer l'entreprise" @click="submitCompany" :disabled="isFetching" />
    </FormWrapper>
  </div>
</template>

<script setup>
import { ref } from "vue"
import FormWrapper from "@/components/FormWrapper"
import { errorRequiredField, firstErrorMsg } from "@/utils/forms"
import { useVuelidate } from "@vuelidate/core"
import { headers } from "@/utils/data-fetching"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { useRootStore } from "@/stores/root"

const rootStore = useRootStore()

// Props & emits
const company = defineModel()
const emit = defineEmits(["changeStep"])

// Form state & rules

const state = ref({
  socialName: "",
  commercialName: "",
  address: "",
  additionalDetails: "",
  postalCode: "",
  city: "",
  cedex: "",
  country: company.value.country,
  // on passe soit un numéro de SIRET, soit de VAT dans le payload
  [company.value.identifierType]: company.value.identifier,
  // activities
  activities: [],
  // contact
  phone_number: "",
  email: "",
  website: "",
})

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
  email: errorRequiredField,
  website: {},
}

const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

// Request definition
const { data, response, execute, isFetching } = useFetch(
  `/api/v1/companies/`,
  {
    headers: headers(),
  },
  { immediate: false }
)
  .post(state)
  .json()

// Request execution
const submitCompany = async () => {
  v$.value.$clearExternalResults()
  v$.value.$validate()
  if (v$.value.$error) {
    return // prevent API call if there is a front-end error
  }
  await execute()
  $externalResults.value = await handleError(response)
  if (response.value.ok) {
    company.value.id = data.value.id
    company.value.socialName = data.value.socialName
    rootStore.fetchInitialData()
    emit("changeStep", {
      name: "L'entreprise a bien été créée",
      component: "EndCompanyCreated",
    })
  }
}

// Data
const allActivities = [
  {
    label: "Fabricant",
    name: "FABRICANT",
    hint: "Le fabricant est responsable de la production des compléments alimentaires.",
  },
  {
    label: "Façonnier",
    name: "FAÇONNIER",
    hint: "Le façonnier (ou sous-traitant) produit des compléments alimentaires pour le compte d'autres marques.",
  },
  {
    label: "Importateur",
    name: "IMPORTATEUR",
    hint: "L'importateur est responsable de l'introduction de compléments alimentaires provenant d'un pays hors UE, sur le marché français.",
  },
  {
    label: "Introducteur",
    name: "INTRODUCTEUR",
    hint: "L'introducteur est responsable de l'introduction de compléments alimentaires provenant d'un pays de l'UE, sur le marché français.",
  },
  {
    label: "Conseil",
    name: "CONSEIL",
    hint: "Ce rôle peut être tenu par des organismes spécialisés (type cabinet de conseil) qui fournissent des expertises et des conseils aux autres acteurs de la chaîne.",
  },
  {
    label: "Distributeur",
    name: "DISTRIBUTEUR",
    hint: "Le distributeur achète des compléments alimentaires pour les revendre aux détaillants ou directement aux consommateurs.",
  },
]
</script>
