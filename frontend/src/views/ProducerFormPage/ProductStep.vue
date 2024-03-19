<template>
  <h2 class="fr-h6">
    <v-icon class="mr-1" name="ri-price-tag-2-fill" />
    Dénomination commerciale
  </h2>
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
  <h2 class="fr-h6 !mt-8">
    <v-icon class="mr-1" name="ri-capsule-fill" />
    Format
  </h2>
  <DsfrInputGroup class="mt-6 max-w-md">
    <DsfrSelect
      label="Forme galénique"
      v-model="payload.galenicFormulation"
      :options="galenicFormulation"
      :required="true"
    />
  </DsfrInputGroup>
  <div class="grid grid-cols-2 gap-4">
    <div class="col-span-2 md:col-span-1 max-w-md">
      <DsfrFieldset legend="Poids ou volume d'une unité de consommation" legendClass="fr-label !font-normal !pb-0">
        <div class="flex">
          <div class="max-w-64">
            <DsfrInput v-model="payload.unitQuantity" class="max-w-64" :required="true" />
          </div>
          <div class="max-w-32 ml-4">
            <DsfrSelect :options="units" v-model="payload.unitMeasurement" defaultUnselectedText="Unité" />
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
    <DsfrInput is-textarea v-model="payload.warnings" label-visible label="Mise en garde et avertissement" />
  </DsfrInputGroup>
  <h2 class="fr-h6 !mt-8">
    <v-icon class="mr-1" name="ri-file-user-fill" />
    Populations cible
  </h2>
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
        <input :id="`condition-${condition.id}`" type="checkbox" v-model="payload.conditions" :value="condition.id" />
        <label :for="`condition-${condition.id}`" class="fr-label ml-2">{{ condition.name }}</label>
      </div>
    </div>
  </DsfrFieldset>
  <h2 class="fr-h6 !mt-8">
    <v-icon class="mr-1" name="ri-focus-2-fill" />
    Objectifs / effets
  </h2>
  <DsfrFieldset>
    <div class="grid grid-cols-6 gap-4 fr-checkbox-group input">
      <div v-for="effect in effects" :key="`effect-${effect}`" class="flex col-span-6 sm:col-span-3 lg:col-span-2">
        <input :id="`effect-${effect}`" type="checkbox" v-model="payload.effects" :value="effect" />
        <label :for="`effect-${effect}`" class="fr-label ml-2">{{ effect }}</label>
      </div>
    </div>
  </DsfrFieldset>
  <DsfrInputGroup class="max-w-2xl mt-6" v-if="payload.effects && payload.effects.indexOf('Autre (à préciser)') > -1">
    <DsfrInput
      v-model="payload.otherEffects"
      label-visible
      label="Merci de préciser les autres objectifs ou effets"
      :required="true"
    />
  </DsfrInputGroup>
  <h2 class="fr-h6 !mt-8">
    <v-icon class="mr-1" name="ri-home-2-fill" />
    Adresse sur l'étiquetage
  </h2>
  TODO car on aura déjà l'adresse à partir du SIRET
</template>
<script setup>
import { defineModel } from "vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"

const payload = defineModel()

const store = useRootStore()
const { populations, conditions, units } = storeToRefs(store)
const galenicFormulation = [
  {
    text: "Ampoule",
    value: "ampoule",
  },
  {
    text: "Comprimé",
    value: "comprime",
  },
]

const effects = [
  "Non défini",
  "Antioxydant",
  "Artères et cholestérol",
  "Articulations",
  "Cheveux et ongles",
  "Circulation sanguine et lymphatique",
  "Concentration",
  "Croissance et developpement",
  "Cycles féminins",
  "Détoxifiant / Draineur",
  "Digestion",
  "Gestion du poids / minceur",
  "Grossesse et allaitement",
  "Humeur",
  "Immunité",
  "Mémoire",
  "Ménopause",
  "Minceur / Brûleur",
  "Minceur / Capteur",
  "Minceur / Glycémie",
  "Minceur / Modérateur d'appétit",
  "Minceur / Ventre plat",
  "Œil / Vision",
  "Os",
  "Peau",
  "Santé bucco-dentaire",
  "Solaire",
  "Sommeil",
  "Sport",
  "Système nerveux",
  "Système urinaire",
  "Tonus sexuel",
  "Transit",
  "Voies respiratoires",
  "Autre (à préciser)",
]
</script>
