<template>
  <div class="mb-8">
    <div class="bg-blue-france-950 py-1">
      <div class="fr-container">
        <DsfrBreadcrumb :links="breadcrumbLinks" />

        <h1 class="-mt-6 mb-4">{{ pageTitle }}</h1>
      </div>
    </div>
    <div class="fr-container">
      <p class="mt-6">
        <v-icon :name="icon" />
        {{ typeName }}
      </p>

      <FormWrapper class="mx-auto">
        <DsfrFieldset legend="Identité de l’ingrédient" legendClass="fr-h4 !mb-0 !pb-2">
          <!-- TODO: validation -->
          <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-x-8">
            <div class="col-span-2 lg:col-span-5" v-if="formForType.name">
              <DsfrInputGroup>
                <DsfrInput v-model="state.name" :label="formForType.name.label" required labelVisible />
              </DsfrInputGroup>
            </div>
            <div class="col-span-2" v-if="formForType.family && plantFamiliesDisplay">
              <DsfrInputGroup>
                <DsfrSelect
                  v-model="state.family"
                  label="Famille de la plante"
                  :options="plantFamiliesDisplay"
                  labelKey="name"
                  required
                />
              </DsfrInputGroup>
            </div>
            <div v-if="formForType.species" class="col-span-2">
              <DsfrInputGroup>
                <DsfrInput v-model="state.species" label="Espèce du micro organisme" labelVisible required />
              </DsfrInputGroup>
            </div>
            <div v-if="formForType.genus" class="col-span-2">
              <DsfrInputGroup>
                <DsfrInput v-model="state.genus" label="Genre" labelVisible required />
              </DsfrInputGroup>
            </div>
            <div class="col-span-2">
              <DsfrInputGroup v-if="formForType.ingredientType">
                <DsfrSelect
                  v-model="state.ingredientType"
                  label="Type de l'ingrédient"
                  :options="ingredientTypes"
                  required
                />
              </DsfrInputGroup>
            </div>

            <DsfrToggleSwitch
              v-model="state.novelFood"
              label="Novel food"
              activeText="Oui"
              inactiveText="Non"
              label-left
              class="self-center mt-4"
            />
            <DsfrToggleSwitch
              v-model="state.status"
              label="Autorisation de l’ingrédient"
              activeText="Authorisé"
              inactiveText="Non authorisé"
              label-left
              class="self-center mt-4"
            />
            <DsfrInputGroup v-if="formForType.einecNumber">
              <DsfrInput v-model="state.einecNumber" label="Numéro EINECS" labelVisible />
            </DsfrInputGroup>
            <DsfrInputGroup v-if="formForType.casNumber">
              <DsfrInput v-model="state.casNumber" label="Numéro CAS" labelVisible />
            </DsfrInputGroup>
          </div>
          <div class="grid md:grid-cols-2 mt-4">
            <DsfrFieldset legend="Synonymes" legendClass="fr-text--lg !pb-0 !mb-2 !mt-4">
              <DsfrInput
                v-for="(_, idx) in state.synonyms"
                :key="`synonym-${idx}`"
                v-model="state.synonyms[idx].name"
                class="mb-4"
              />
              <DsfrButton
                label="Ajouter un synonyme"
                @click="addNewSynonym"
                icon="ri-add-line"
                size="sm"
                class="mt-2"
                secondary
              />
            </DsfrFieldset>
          </div>
        </DsfrFieldset>
        <DsfrFieldset legend="Utilisation de l’ingrédient" legendClass="fr-h4 !mb-0 !pb-2">
          <div v-if="formForType.plantParts" class="grid md:grid-cols-3 items-end my-4 md:my-2">
            <DsfrMultiselect
              v-model="state.plantParts"
              :options="plantParts"
              label="Partie(s) utilisée(s)"
              search
              labelKey="name"
            />
            <div class="md:ml-4 md:my-8 md:col-span-2">
              <DsfrTag
                v-for="id in state.plantParts"
                :key="id"
                :label="optionLabel(plantParts, id)"
                class="mx-1"
              ></DsfrTag>
            </div>
          </div>
          <div v-if="formForType.substances" class="grid md:grid-cols-3 items-end my-4 md:my-2">
            <!-- TODO: option to create new active substance -->
            <ElementAutocomplete
              autocomplete="nothing"
              label="Substances actives"
              label-visible
              class="max-w-md grow mb-3"
              hint="Tapez au moins trois caractères pour démarrer la recherche"
              :hideSearchButton="true"
              @selected="selectOption"
              type="substance"
            />
            <div class="md:ml-4 md:my-7 md:col-span-2">
              <!-- TODO: make tags deleteable -->
              <DsfrTag
                v-for="substance in state.substances"
                :key="substance.id"
                :label="substance.name"
                class="mx-1"
              ></DsfrTag>
            </div>
          </div>
          <div class="grid grid-cols-3 gap-x-8" v-if="formForType.nutritionalReference">
            <div>
              <NumberField
                label="Apport nutritionnel de référence"
                label-visible
                v-model="state.nutritionalReference"
              />
            </div>
            <div>
              <NumberField label="Quantité maximale autorisée" label-visible v-model="state.maxQuantity" />
            </div>
            <div class="max-w-32">
              <DsfrSelect
                label="Unité"
                label-visible
                required
                :options="store.units?.map((unit) => ({ text: unit.name, value: unit.id }))"
                v-model="state.unit"
                defaultUnselectedText="Unité"
              />
            </div>
          </div>
          <p class="my-4"><i>Population cible et à risque en construction</i></p>
        </DsfrFieldset>
        <DsfrFieldset legend="Commentaires" legendClass="fr-h4 !mb-0">
          <div class="grid md:grid-cols-2 md:gap-4">
            <div class="mb-4">
              <DsfrInput label="Commentaire public" v-model="state.publicComments" :isTextarea="true" label-visible />
            </div>
            <div class="mb-4">
              <DsfrInput label="Commentaire privé" v-model="state.privateComments" :isTextarea="true" label-visible />
            </div>
          </div>
        </DsfrFieldset>
        <div class="flex gap-x-2 mt-4">
          <DsfrButton label="Enregistrer ingrédient" @click="saveElement" :disabled="isFetching" />
        </div>
      </FormWrapper>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { getTypeIcon, getTypeInFrench, unSlugifyType, getApiType } from "@/utils/mappings"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
// import { firstErrorMsg } from "@/utils/forms"
import { /*useRoute,*/ useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import { handleError } from "@/utils/error-handling"
import useToaster from "@/composables/use-toaster"
import FormWrapper from "@/components/FormWrapper"
import ElementAutocomplete from "@/components/ElementAutocomplete"
import NumberField from "@/components/NumberField"

// TODO: make type changeable and prefillable via query param
const type = ref("ingredient")
const icon = computed(() => getTypeIcon(type.value))
const typeName = computed(() => getTypeInFrench(type.value))
const router = useRouter()

const pageTitle = "Création élément" // eventually will be computed on the action (create/modify)

const breadcrumbLinks = computed(() => {
  const links = [{ to: { name: "DashboardPage" }, text: "Tableau de bord" }]
  links.push({ text: pageTitle })
  return links
})

const EMPTY_SYNONYM = { name: "" }
const newSynonym = () => JSON.parse(JSON.stringify(EMPTY_SYNONYM))

const state = ref({
  plantParts: [],
  substances: [],
  synonyms: [newSynonym(), newSynonym(), newSynonym()],
})

const isFetching = false // TODO: set to true when fetching data or sending update, see CompanyForm

const saveElement = async () => {
  // TODO: validate form before anything else
  const url = `/api/v1/${getApiType(type.value)}s/`
  const payload = state.value
  if (payload.substances.length) {
    payload.substances = payload.substances.map((substance) => substance.id)
  }
  payload.synonyms = payload.synonyms.filter((s) => !!s.name)
  payload.status = payload.status ? 1 : 2
  const { response } = await useFetch(url, { headers: headers() }).post(payload).json()
  await handleError(response)
  if (response.value.ok) {
    useToaster().addMessage({
      type: "success",
      id: "element-creation-success",
      description: "L'élément a été créé",
    })
    router.push({ name: "DashboardPage" })
  }
}
const addNewSynonym = async () => {
  state.value.synonyms.push(newSynonym())
}

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
    // novelFood is true for every type TODO: not for aromes
    plantParts: true,
    substances: true,
    // population cible: true for everyone also not yet in our database
    // public notes true for every type
  },
  substance: {
    name: {
      label: "Nom de la substance",
    },
    einecNumber: true,
    casNumber: true,
    nutritionalReference: true,
    maxQuantity: true,
    unit: true,
  },
  microorganism: {
    species: true,
    genus: true,
    function: true,
    substances: true,
  },
  default: {
    name: {
      label: "Nom ingrédient",
    },
    ingredientType: true,
    function: true,
    substances: true,
  },
}
const formForType = computed(() => {
  return formQuestions[type.value] || formQuestions.default
})

const store = useRootStore()
const { plantParts, plantFamilies } = storeToRefs(store)
store.fetchDeclarationFieldsData()
store.fetchPlantFamilies()

const ingredientTypes = [
  { value: 1, text: "Nutriment (Forme d'apport)" },
  { value: 2, text: "Additif" },
  { value: 3, text: "Arôme" },
  { value: 4, text: "Autre ingrédient actif" },
  { value: 5, text: "Autre ingrédient" },
]

const selectOption = async (result) => {
  state.value.substances.push(result)
}

const optionLabel = (options, id) => {
  return options.find((o) => o.id === id)?.name || "Inconnu"
}

const plantFamiliesDisplay = computed(() => {
  return plantFamilies.value?.map((family) => ({ value: family.id, text: family.name }))
})
</script>
