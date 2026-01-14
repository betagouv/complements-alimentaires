<template>
  <div>
    <!-- Si on a une seule entreprise, pas besoin d'afficher ce champ -->
    <template v-if="!companies || companies.length !== 1">
      <SectionTitle title="Entreprise" sizeTag="h6" icon="ri-home-2-fill" />
      <DsfrAlert type="warning" v-if="!companies || companies.length === 0">
        <p>
          Vous n'avez pas d'entreprise assignée. Contacter l'administrateur de votre entreprise ou
          <router-link :to="{ name: 'Root' }">ajoutez une entreprise</router-link>
          .
        </p>
      </DsfrAlert>
      <DsfrInputGroup class="max-w-md" :error-message="firstErrorMsg(v$, 'company')" v-else>
        <DsfrSelect
          label="Entreprise responsable de mise sur le marché du complément"
          v-model="selectedCompanyOption"
          :options="companiesSelectOptions"
          :required="true"
        />
      </DsfrInputGroup>
    </template>

    <SectionTitle title="Dénomination commerciale" class="mt-10!" sizeTag="h6" icon="ri-price-tag-2-fill" />
    <div class="grid grid-cols-2 gap-4">
      <div class="col-span-2 md:col-span-1 max-w-md">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'name')">
          <DsfrInput v-model="payload.name" label-visible label="Nom du produit" :required="true" />
        </DsfrInputGroup>
      </div>
      <div class="col-span-2 md:col-span-1 max-w-md">
        <DsfrInputGroup>
          <DsfrInput v-model="payload.brand" label-visible label="Marque" />
        </DsfrInputGroup>
      </div>
      <div class="col-span-2 md:col-span-1 max-w-md">
        <DsfrInputGroup>
          <DsfrInput v-model="payload.gamme" label-visible label="Gamme" />
        </DsfrInputGroup>
      </div>
      <div class="col-span-2 md:col-span-1 max-w-md">
        <DsfrInputGroup>
          <DsfrInput v-model="payload.flavor" label-visible label="Arôme" />
        </DsfrInputGroup>
      </div>
      <DsfrInputGroup class="max-w-2xl mt-6">
        <DsfrInput is-textarea v-model="payload.description" label-visible label="Description" />
      </DsfrInputGroup>
    </div>
    <SectionTitle title="Format" class="mt-10!" sizeTag="h6" icon="ri-capsule-fill" />
    <DsfrFieldset legend="Forme galénique">
      <div class="sm:grid grid-cols-2 gap-4">
        <div class="sm:flex">
          <div class="sm:max-w-32 sm:mr-4 mb-4 sm:mb-0">
            <DsfrSelect :required="true" label="État" :options="formulationStates" v-model="galenicFormulationState" />
          </div>
          <div class="max-w-md mb-4 sm:mb-0">
            <DsfrSelect
              :required="true"
              :disabled="!galenicFormulationState"
              label="Forme"
              v-model="payload.galenicFormulation"
              :options="
                galenicFormulationList?.map((formulation) => ({
                  text: formulation.name,
                  value: formulation.id,
                }))
              "
            />
          </div>
        </div>
        <div class="max-w-2xl pt-0">
          <DsfrInput
            v-if="
              payload.galenicFormulation &&
              galenicFormulations &&
              getAllIndexesOfRegex(galenicFormulations, /Autre.*(à préciser)/).includes(
                parseInt(payload.galenicFormulation)
              )
            "
            v-model="payload.otherGalenicFormulation"
            label-visible
            label="Merci de préciser la forme galénique"
            :required="true"
          />
        </div>
      </div>
    </DsfrFieldset>

    <div class="grid grid-cols-2 gap-4">
      <div class="col-span-2 md:col-span-1 max-w-md mt-6">
        <DsfrFieldset legend="Poids ou volume d'une unité de consommation">
          <div class="sm:flex">
            <div class="max-w-64 mb-4 sm:mb-0">
              <NumberField
                label="Quantité"
                label-visible
                v-model="payload.unitQuantity"
                class="max-w-64"
                :required="true"
              />
            </div>
            <div class="max-w-32 sm:ml-4">
              <DsfrSelect
                label="Unité"
                label-visible
                :required="true"
                :options="store.units?.map((unit) => ({ text: unit.name, value: unit.id }))"
                v-model="payload.unitMeasurement"
                defaultUnselectedText="Unité"
              />
            </div>
          </div>
        </DsfrFieldset>
      </div>
      <div class="col-span-2 md:col-span-1 max-w-md pt-0 sm:pt-12">
        <DsfrInputGroup>
          <DsfrInput v-model="payload.conditioning" label-visible label="Conditionnement" />
        </DsfrInputGroup>
      </div>
    </div>
    <div class="grid grid-cols-2 gap-4">
      <div class="col-span-2 md:col-span-1 max-w-md">
        <DsfrInputGroup>
          <DsfrInput
            v-model="payload.dailyRecommendedDose"
            label-visible
            label="Dose journalière recommandée"
            :required="true"
          />
        </DsfrInputGroup>
      </div>
      <div class="col-span-2 md:col-span-1 max-w-md">
        <DsfrInputGroup>
          <DsfrInput
            :required="true"
            v-model="payload.minimumDuration"
            label-visible
            label="Durabilité minimale / DLUO (en mois)"
          />
        </DsfrInputGroup>
      </div>
    </div>
    <DsfrInputGroup class="max-w-2xl mt-6">
      <DsfrInput v-model="payload.instructions" label-visible label="Mode d'emploi" />
    </DsfrInputGroup>
    <SectionTitle title="Populations cibles et à risque" class="mt-10!" sizeTag="h6" icon="ri-file-user-fill" />
    <PopulationsCheckboxes v-model="payload.populations" :populations="populations" />
    <ConditionsCheckboxes v-model="payload.conditionsNotRecommended" :conditions="conditions" />

    <OtherChoiceField
      :listOfChoices="payload.conditionsNotRecommended"
      v-model="payload.otherConditions"
      :otherChoiceId="otherConditionId"
      label="Merci de préciser les autres populations à risques ou facteurs de risques"
    ></OtherChoiceField>

    <DsfrInputGroup class="max-w-2xl mt-6">
      <DsfrInput is-textarea v-model="payload.warning" label-visible label="Mise en garde et avertissement" />
    </DsfrInputGroup>

    <SectionTitle title="Objectifs / effets" class="mt-10!" sizeTag="h6" icon="ri-focus-2-fill" />
    <DsfrFieldset>
      <div class="grid grid-cols-6 gap-4 fr-checkbox-group input">
        <div
          v-for="effect in orderedEffects"
          :key="`effect-${effect.id}`"
          class="flex col-span-6 sm:col-span-3 lg:col-span-2"
        >
          <input :id="`effect-${effect.id}`" type="checkbox" v-model="payload.effects" :value="effect.id" />
          <label :for="`effect-${effect.id}`" class="fr-label">{{ effect.name }}</label>
        </div>
      </div>
    </DsfrFieldset>
    <OtherChoiceField
      :listOfChoices="payload.effects"
      v-model="payload.otherEffects"
      :otherChoiceId="otherEffectsId"
      label="Merci de préciser les autres objectifs ou effets"
    ></OtherChoiceField>

    <SectionTitle title="Adresse sur l'étiquetage" class="mt-10!" sizeTag="h6" icon="ri-home-2-fill" />
    <div class="max-w-2xl mb-8 address-form">
      <DsfrInputGroup>
        <DsfrInput v-model="payload.address" label-visible label="Adresse" hint="Numéro et voie" :required="true" />
      </DsfrInputGroup>
      <DsfrInputGroup>
        <DsfrInput
          v-model="payload.additionalDetails"
          label-visible
          label="Complément d'adresse"
          hint="Bâtiment, immeuble, escalier et numéro d’appartement"
        />
      </DsfrInputGroup>
      <div class="grid grid-cols-12 gap-6">
        <div class="col-span-12 md:col-span-4">
          <DsfrInputGroup>
            <DsfrInput v-model="payload.postalCode" label-visible label="Code Postal" :required="true" />
          </DsfrInputGroup>
        </div>
        <div class="col-span-12 md:col-span-5">
          <DsfrInputGroup>
            <DsfrInput v-model="payload.city" label-visible label="Ville ou commune" :required="true" />
          </DsfrInputGroup>
        </div>
      </div>
      <DsfrInputGroup>
        <DsfrInput v-model="payload.cedex" label-visible label="Cedex" />
      </DsfrInputGroup>
      <DsfrInputGroup>
        <CountryField v-model="payload.country" :required="true" />
      </DsfrInputGroup>
    </div>
  </div>
</template>
<script setup>
import { computed, watch, ref } from "vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { useVuelidate } from "@vuelidate/core"
import { firstErrorMsg, transformArrayByColumn, checkboxColumnNumbers } from "@/utils/forms"
import { useCurrentBreakpoint } from "@/utils/screen"
import { pushOtherChoiceFieldAtTheEnd, getAllIndexesOfRegex } from "@/utils/forms"
import CountryField from "@/components/fields/CountryField.vue"
import OtherChoiceField from "@/components/fields/OtherChoiceField"
import SectionTitle from "@/components/SectionTitle"
import NumberField from "@/components/NumberField"
import PopulationsCheckboxes from "./PopulationsCheckboxes"
import ConditionsCheckboxes from "./ConditionsCheckboxes"

const payload = defineModel()
const props = defineProps(["externalResults"])

// Règle placebo pour ce bug vuelidate :https://github.com/vuelidate/vuelidate/issues/1209
// Il est également nécessaire de mettre l'$autovalidate et le $watch avec le $touch pour faire
// ressortir les erreurs du `silentErrors`
const externalServerValidation = () => true
const rules = {
  company: { externalServerValidation, $autovalidate: true },
  name: { externalServerValidation, $autovalidate: true },
}
const $externalResults = computed(() => props.externalResults)
const v$ = useVuelidate(rules, payload, { $externalResults })
watch($externalResults, () => v$.value.$touch())

const store = useRootStore()
const { populations, conditions, effects, galenicFormulations, loggedUser } = storeToRefs(store)

const galenicFormulationState = ref(null)
// Peupler la variable du state si la forme galénique est présente déjà dans le payload
const populateGalenicFormulationState = () => {
  if (payload.value.galenicFormulation) {
    const formulation = galenicFormulations.value?.find((x) => x.id === payload.value.galenicFormulation)
    if (formulation) galenicFormulationState.value = formulation.isLiquid ? "liquid" : "solid"
  }
}
watch(galenicFormulations, populateGalenicFormulationState, { immediate: true })

const otherConditionId = computed(() => conditions.value?.find((effect) => effect.name === "Autre (à préciser)")?.id)
const otherEffectsId = computed(() => effects.value?.find((effect) => effect.name === "Autre (à préciser)")?.id)
const galenicFormulationList = computed(() => {
  if (!galenicFormulationState.value) return galenicFormulations.value
  else {
    const isLiquid = galenicFormulationState.value === "liquid"
    return pushOtherChoiceFieldAtTheEnd(
      galenicFormulations.value
        ?.filter((formulation) => formulation.isLiquid === isLiquid) // le filter perd l'ordre alphabétique d'origine
        .sort((a, b) => a.name.localeCompare(b.name))
    )
  }
})

const formulationStates = [
  {
    text: "Liquide",
    value: "liquid",
  },
  {
    text: "Solide",
    value: "solid",
  },
]

// Gestion d'entreprises / mandataires
const companies = computed(() =>
  loggedUser.value.companies.filter((company) => company.roles.some((role) => role.name === "DeclarantRole"))
)

const companiesSelectOptions = computed(() => {
  return companies.value?.map((x) => ({
    text: `${x.socialName} ${x.representedBy ? "(représenté par " + x.representedBy.socialName + ")" : ""}`,

    // Pour distinguer les combinaisons entre entreprise et entreprise mandatée on utilise une combinaison d'ID :
    // "<id de la compagnie>|<id de l'entreprise mandataire (s'il y en a)>"
    value: `${x.id}|${x.representedBy?.id || ""}`,
  }))
})

const selectedCompanyOption = ref(`${payload.value.company}|${payload.value.mandatedCompany || ""}`)
watch(selectedCompanyOption, (value) => {
  const [companyId, mandatedCompanyId] = value?.split?.("|") || [null, null]
  payload.value.company = companyId ? parseInt(companyId) : null
  payload.value.mandatedCompany = mandatedCompanyId ? parseInt(mandatedCompanyId) : null
})

const selectedCompany = computed(() => companies.value?.find((x) => x.id === payload.value.company))
watch(selectedCompany, () => {
  const addressFields = ["address", "additionalDetails", "postalCode", "city", "cedex", "country"]
  const addressEmpty = addressFields.every((field) => !payload.value[field])
  if (addressEmpty && selectedCompany.value)
    addressFields.forEach((field) => (payload.value[field] = selectedCompany.value[field]))
})

// S'il n'y a qu'une entreprise on l'assigne par défaut
if (companies.value?.length === 1) payload.value.company = companies.value[0].id

const currentBreakpoint = useCurrentBreakpoint()
const numberOfColumns = computed(() => checkboxColumnNumbers[currentBreakpoint.value])
const orderedEffects = computed(() => transformArrayByColumn(effects.value, numberOfColumns.value))
</script>

<style scoped>
@reference "../../styles/index.css";

.address-form .fr-input-group:not(:last-child) {
  @apply mb-0;
}
</style>
