<template>
  <div class="fr-container mb-8">
    <DsfrBreadcrumb class="mb-8" :links="breadcrumbLinks" />

    <h1>Modification élément</h1>

    <p>
      <v-icon :name="icon" />
      {{ typeName }}
    </p>

    <!-- TODO: tabs -->
    <FormWrapper class="mx-auto">
      <DsfrFieldset legend="Identité de l’ingrédient" legendClass="fr-h4">
        <!-- TODO: validation -->
        <div class="flex gap-x-4 -mb-8">
          <DsfrInputGroup>
            <DsfrInput v-model="state.caName" :label="formForType.name.label" required labelVisible />
          </DsfrInputGroup>
          <DsfrInputGroup v-if="formForType.family">
            <!-- Question: multiselect or single? -->
            <DsfrSelect v-model="state.caFamily" label="Famille de la plante" :options="plantFamilies" required />
          </DsfrInputGroup>
          <DsfrInputGroup v-if="formForType.function">
            <!-- Question: multiselect or single? -->
            <!-- Question: do we have this in the DB? -->
            <DsfrSelect v-model="state.function" label="Fonction de l'ingrédient" :options="functions" required />
          </DsfrInputGroup>

          <DsfrToggleSwitch
            v-model="state.authorised"
            label="Authoriser l'ingrédient"
            activeText="Authorisé"
            inactiveText="Non authorisé"
            label-left
            class="self-center"
          />
        </div>
        <DsfrInputGroup>
          <DsfrInput v-model="state.description" label="Description" labelVisible />
        </DsfrInputGroup>
        <DsfrFieldset legend="Synonymes" legendClass="fr-text--lg">
          <ul>
            <li v-for="(synonym, idx) in synonyms" :key="idx">{{ synonym.label }}, {{ synonym.type }}</li>
          </ul>
          <!-- TODO: table -->
          <!-- TODO: delete/edit per line -->
          <!-- TODO: add new line -->
          <!-- TODO: if new, three ? editable lines by default -->
          <DsfrButton label="Ajouter un synonyme" @click="addNewSynonym" icon="ri-add-line" size="sm" />
        </DsfrFieldset>
        <!-- name: {
            label: "Nom de la plante",
          },
          family: true,
          function: true,
          // authorise: true for every type
          // description is true for every type -->
      </DsfrFieldset>
      <DsfrFieldset legend="Utilisation de l’ingrédient" legendClass="fr-h4">
        <!-- usedParts: true,
        activeSubstances: true,
        // population cible: true for everyone also not yet in our database -->
      </DsfrFieldset>
      <DsfrFieldset legend="Commentaire à destination du public" legendClass="fr-h4"></DsfrFieldset>
      <div class="flex gap-x-2 mt-4">
        <!-- Question: cancel button? -->
        <!-- Question: use DsfrButtonGroup? -->
        <DsfrButton label="Enregistrer ingrédient" @click="saveElement" :disabled="isFetching" />
        <DsfrButton label="Sauvegarder brouillon" @click="saveAsDraft" :disabled="isFetching" secondary />
      </div>
    </FormWrapper>
  </div>
</template>

<script setup>
import { /*ref, */ computed /*, watch*/ } from "vue"
import { getTypeIcon, getTypeInFrench, unSlugifyType /*, getApiType*/ } from "@/utils/mappings"
// import { firstErrorMsg } from "@/utils/forms"
// import { useRoute, useRouter } from "vue-router"
// import { useFetch } from "@vueuse/core"
// import { handleError } from "@/utils/error-handling"
import FormWrapper from "@/components/FormWrapper"

const props = defineProps({ urlComponent: String })
const elementId = computed(() => props.urlComponent.split("--")[0])
const type = computed(() => unSlugifyType(props.urlComponent.split("--")[1]))
const icon = computed(() => getTypeIcon(type.value))
const typeName = computed(() => getTypeInFrench(type.value))

const breadcrumbLinks = computed(() => {
  const links = [{ to: { name: "DashboardPage" }, text: "Tableau de bord" }]
  links.push({ text: `Modification élément ${elementId.value}` })
  return links
})

const state = {} // TODO: prefill with existing data if modifying

const isFetching = false // TODO: set to true when fetching data or sending update, see CompanyForm

const saveElement = async () => {}
const saveAsDraft = async () => {}
const addNewSynonym = async () => {}

const formQuestions = {
  plant: {
    name: {
      label: "Nom de la plante",
    },
    family: true,
    function: true,
    // authorise: true for every type
    // description is true for every type
    // synonymes are true for every type
    usedParts: true,
    activeSubstances: true,
    // population cible: true for everyone also not yet in our database
    // public notes true for every type
  },
  substance: {
    name: {
      label: "Nom de la substance",
    },
    nameEn: {
      label: "Nom de la substance en anglais",
    },
    substanceType: true,
    einecsNumber: true,
    casNumber: true,
    source: true,
    sourceEn: true,
  },
  microorganism: {
    name: {
      label: "Espèce du micro organisme",
    },
    genre: true,
    function: true,
    activeSubstances: true,
  },
  default: {
    name: {
      label: "Nom ingrédient",
    },
    nameEn: {
      label: "Nom ingrédient en anglais",
    },
    ingredientType: true,
    function: true,
    activeSubstances: true,
  },
}
const formForType = computed(() => {
  return formQuestions.plant // TODO: choose based on type
})

const plantFamilies = [] // TODO: fetch options from DB
const functions = [] // TODO: fetch options from DB

const synonyms = [
  { label: "Example", type: "Nom en anglais" },
  { label: "Cassius", type: "Nom en latin" },
]
</script>
