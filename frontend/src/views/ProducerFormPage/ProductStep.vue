<template>
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
    <DsfrInputGroup class="max-w-md" v-else>
      <DsfrSelect
        label="Entreprise qui produit le complément"
        v-model.number="payload.company"
        :options="companies.map((x) => ({ text: x.socialName, value: x.id }))"
        :required="true"
      />
    </DsfrInputGroup>
  </template>

  <SectionTitle title="Dénomination commerciale" class="!mt-10" sizeTag="h6" icon="ri-price-tag-2-fill" />
  <div class="grid grid-cols-2 gap-4">
    <div class="col-span-2 md:col-span-1 max-w-md">
      <DsfrInputGroup>
        <DsfrInput v-model="payload.name" label-visible label="Nom du produit" :required="true" />
      </DsfrInputGroup>
      <DsfrInputGroup>
        <DsfrInput v-model="payload.brand" label-visible label="Marque" />
      </DsfrInputGroup>
    </div>
    <div class="col-span-2 md:col-span-1 max-w-md">
      <!-- Useless? -->
      <DsfrInputGroup>
        <DsfrInput v-model="payload.gamme" label-visible label="Gamme" />
      </DsfrInputGroup>

      <!-- Useless? -->
      <DsfrInputGroup>
        <DsfrInput v-model="payload.flavor" label-visible label="Arôme" />
      </DsfrInputGroup>
    </div>
    <DsfrInputGroup class="max-w-2xl mt-6">
      <DsfrInput is-textarea v-model="payload.description" label-visible label="Description" :required="true" />
    </DsfrInputGroup>
  </div>
  <SectionTitle title="Format" class="!mt-10" sizeTag="h6" icon="ri-capsule-fill" />
  <div class="grid grid-cols-2 gap-4">
    <DsfrFieldset legend="Forme galénique" legendClass="fr-label !font-normal !pb-0">
      <div class="flex">
        <div class="max-w-32">
          <DsfrSelect :options="formulationStates" v-model="galenicFormulationState" defaultUnselectedText="État" />
        </div>
        <div class="max-w-md ml-4">
          <DsfrSelect
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
    </DsfrFieldset>
    <div class="max-w-2xl">
      <DsfrInput
        v-if="
          payload.galenicFormulation &&
          galenicFormulation &&
          getAllIndexesOfRegex(galenicFormulation, /Autre.*(à préciser)/).includes(parseInt(payload.galenicFormulation))
        "
        v-model="payload.otherGalenicFormulation"
        label-visible
        label="Merci de préciser la forme galénique"
      />
    </div>
  </div>

  <div class="grid grid-cols-2 gap-4">
    <div class="col-span-2 md:col-span-1 max-w-md mt-6">
      <DsfrFieldset legend="Poids ou volume d'une unité de consommation" legendClass="fr-label !font-normal !pb-0">
        <div class="flex">
          <div class="max-w-64">
            <DsfrInput v-model="payload.unitQuantity" class="max-w-64" :required="true" />
          </div>
          <div class="max-w-32 ml-4">
            <DsfrSelect
              :options="store.units?.map((unit) => ({ text: unit.name, value: unit.id }))"
              v-model="payload.unitMeasurement"
              defaultUnselectedText="Unité"
            />
          </div>
        </div>
      </DsfrFieldset>
    </div>
    <div class="col-span-2 md:col-span-1 max-w-md">
      <DsfrInputGroup>
        <DsfrInput v-model="payload.conditioning" label-visible label="Conditionnements" />
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
        <DsfrInput v-model="payload.minimumDuration" label-visible label="Durabilité minimale / DLUO (en mois)" />
      </DsfrInputGroup>
    </div>
  </div>
  <DsfrInputGroup class="max-w-2xl mt-6">
    <DsfrInput v-model="payload.instructions" label-visible label="Mode d'emploi" />
  </DsfrInputGroup>
  <DsfrInputGroup class="max-w-2xl mt-6">
    <DsfrInput is-textarea v-model="payload.warning" label-visible label="Mise en garde et avertissement" />
  </DsfrInputGroup>
  <SectionTitle title="Populations cible" class="!mt-10" sizeTag="h6" icon="ri-file-user-fill" />
  <DsfrFieldset legend="Population cible" legendClass="fr-label">
    <div class="grid grid-cols-6 gap-4 fr-checkbox-group input">
      <div
        v-for="population in populations"
        :key="`effect-${population.id}`"
        class="flex col-span-6 sm:col-span-3 lg:col-span-2"
      >
        <input
          :id="`population-${population.id}`"
          type="checkbox"
          v-model="payload.populations"
          :value="population.id"
        />
        <label :for="`population-${population.id}`" class="fr-label ml-2">{{ population.name }}</label>
      </div>
    </div>
  </DsfrFieldset>

  <DsfrFieldset legend="Consommation déconseillée" legendClass="fr-label">
    <div class="grid grid-cols-6 gap-4 fr-checkbox-group input">
      <div
        v-for="condition in conditions"
        :key="`condition-${condition.id}`"
        class="flex col-span-6 sm:col-span-3 lg:col-span-2"
      >
        <input
          :id="`condition-${condition.id}`"
          type="checkbox"
          v-model="payload.conditionsNotRecommended"
          :value="condition.id"
        />
        <label :for="`condition-${condition.id}`" class="fr-label ml-2">{{ condition.name }}</label>
      </div>
    </div>
  </DsfrFieldset>
  <SectionTitle title="Objectifs / effets" class="!mt-10" sizeTag="h6" icon="ri-focus-2-fill" />
  <DsfrFieldset>
    <div class="grid grid-cols-6 gap-4 fr-checkbox-group input">
      <div v-for="effect in effects" :key="`effect-${effect.id}`" class="flex col-span-6 sm:col-span-3 lg:col-span-2">
        <input :id="`effect-${effect.id}`" type="checkbox" v-model="payload.effects" :value="effect.id" />
        <label :for="`effect-${effect.id}`" class="fr-label ml-2">{{ effect.name }}</label>
      </div>
    </div>
  </DsfrFieldset>

  <DsfrInputGroup class="max-w-2xl mt-6" v-if="payload.effects && payload.effects.indexOf(otherEffectsId) > -1">
    <DsfrInput
      v-model="payload.otherEffects"
      label-visible
      label="Merci de préciser les autres objectifs ou effets"
      :required="true"
    />
  </DsfrInputGroup>
  <SectionTitle title="Adresse sur l'étiquetage" class="!mt-10" sizeTag="h6" icon="ri-home-2-fill" />
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
    <div class="grid grid-cols-7 gap-6">
      <DsfrInputGroup class="col-span-12 md:col-span-3">
        <DsfrInput v-model="payload.postalCode" label-visible label="Code Postal" :required="true" />
      </DsfrInputGroup>
      <DsfrInputGroup class="col-span-12 md:col-span-4">
        <DsfrInput v-model="payload.city" label-visible label="Ville ou commune" :required="true" />
      </DsfrInputGroup>
    </div>
    <DsfrInputGroup>
      <DsfrInput v-model="payload.cedex" label-visible label="Cedex" />
    </DsfrInputGroup>
    <DsfrInputGroup>
      <CountryField v-model="payload.country" />
    </DsfrInputGroup>
  </div>
</template>
<script setup>
import { computed, watch, ref } from "vue"
import { defineModel } from "vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { otherFieldsAtTheEnd, getAllIndexesOfRegex } from "@/utils/forms"
import CountryField from "@/components/fields/CountryField.vue"
import SectionTitle from "@/components/SectionTitle"

const payload = defineModel()
const store = useRootStore()
const { populations, conditions, effects, galenicFormulation, loggedUser } = storeToRefs(store)
const galenicFormulationState = ref(null)
const otherEffectsId = computed(() => effects.value?.find((effect) => effect.name === "Autre (à préciser)")?.id)
const galenicFormulationList = computed(() => {
  if (!galenicFormulationState.value) return galenicFormulation.value
  else {
    const isLiquid = galenicFormulationState.value === "liquid"
    return otherFieldsAtTheEnd(
      galenicFormulation.value
        ?.filter((formulation) => formulation.isLiquid === isLiquid) // le filter perd l'ordre alphabétique d'origine
        .sort((a, b) => a.name.localeCompare(b.name))
    )
  }
})
const companies = computed(() => loggedUser.value.roles.find((x) => x.name === "Declarant")?.companies)
const selectedCompany = computed(() => companies.value?.find((x) => x.id === payload.value.company))
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
watch(selectedCompany, () => {
  const addressFields = ["address", "additionalDetails", "postalCode", "city", "cedex", "country"]
  const addressEmpty = addressFields.every((field) => !payload.value[field])
  if (addressEmpty && selectedCompany.value)
    addressFields.forEach((field) => (payload.value[field] = selectedCompany.value[field]))
})

// S'il n'y a qu'une entreprise on l'assigne par défaut
if (companies.value?.length === 1) payload.value.company = companies.value[0].id
</script>

<style scoped>
.address-form .fr-input-group:not(:last-child) {
  @apply mb-0;
}
</style>
