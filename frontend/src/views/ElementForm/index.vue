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

      <!-- TODO: tabs -->
      <FormWrapper class="mx-auto">
        <DsfrFieldset legend="Identité de l’ingrédient" legendClass="fr-h4">
          <!-- TODO: validation -->
          <!-- TODO: responsiveness -->
          <div class="flex gap-x-4">
            <div class="flex-1">
              <DsfrInputGroup>
                <DsfrInput v-model="state.name" :label="formForType.name.label" required labelVisible />
              </DsfrInputGroup>
            </div>
            <div class="flex-1">
              <DsfrInputGroup v-if="formForType.family && plantFamiliesDisplay">
                <!-- Question: multiselect or single? -->
                <DsfrSelect
                  v-model="state.family"
                  label="Famille de la plante"
                  :options="plantFamiliesDisplay"
                  labelKey="name"
                  required
                />
              </DsfrInputGroup>
            </div>
            <!-- TODO: add species -->
            <DsfrInputGroup v-if="formForType.genre">
              <DsfrInput v-model="state.genre" label="Genre" labelVisible />
            </DsfrInputGroup>
            <DsfrInputGroup v-if="formForType.ingredientType">
              <!-- Question: multiselect or single? -->
              <!-- Question: do we have this in the DB? -->
              <DsfrSelect v-model="state.ingredientType" label="Type ingrédient" :options="ingredientTypes" required />
            </DsfrInputGroup>
            <DsfrInputGroup v-if="formForType.substanceType">
              <!-- Question: multiselect or single? -->
              <!-- Question: do we have this in the DB? -->
              <DsfrSelect v-model="state.substanceType" label="Type de substance" :options="substanceTypes" required />
            </DsfrInputGroup>

            <DsfrToggleSwitch
              v-model="state.authorised"
              label="Autorisation de l’ingrédient"
              activeText="Authorisé"
              inactiveText="Non authorisé"
              label-left
              class="self-center"
            />
          </div>
          <div class="flex gap-x-4">
            <DsfrInputGroup v-if="formForType.einecsNumber">
              <DsfrInput v-model="state.einecsNumber" label="Numéro EINECS" labelVisible />
            </DsfrInputGroup>
            <DsfrInputGroup v-if="formForType.casNumber">
              <DsfrInput v-model="state.casNumber" label="Numéro CAS" labelVisible />
            </DsfrInputGroup>
            <DsfrInputGroup v-if="formForType.source">
              <DsfrInput v-model="state.source" label="Source" labelVisible />
            </DsfrInputGroup>
          </div>
          <div class="grid md:grid-cols-2">
            <DsfrFieldset legend="Synonymes" legendClass="fr-text--lg !pb-0 !mb-2 !mt-4">
              <DsfrInput
                v-for="(_, idx) in state.synonyms"
                :key="`synonym-${idx}`"
                v-model="state.synonyms[idx].name"
                class="mb-4"
              />
              <!-- TODO: delete/edit per line -->
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
        <DsfrFieldset legend="Utilisation de l’ingrédient" legendClass="fr-h4 !pb-0">
          <div v-if="formForType.plantParts" class="flex items-center my-4">
            <DsfrMultiselect
              v-model="state.plantParts"
              :options="plantParts"
              label="Partie(s) utilisée(s)"
              search
              labelKey="name"
            />
            <div class="ml-4">
              <DsfrTag
                v-for="id in state.plantParts"
                :key="id"
                :label="optionLabel(plantParts, id)"
                class="mx-1"
              ></DsfrTag>
            </div>
          </div>
          <div v-if="formForType.substances" class="flex items-center my-4">
            <!-- TODO: option to create new active substance -->
            <ElementAutocomplete
              autocomplete="nothing"
              label="Substances actives"
              label-visible
              class="max-w-md grow"
              hint="Tapez au moins trois caractères pour démarrer la recherche"
              :hideSearchButton="true"
              @selected="selectOption"
              type="substance"
            />
            <div class="ml-4">
              <!-- TODO: align tags with input -->
              <!-- TODO: filter to only include substances -->
              <!-- TODO: make tags deleteable -->
              <DsfrTag
                v-for="substance in state.substances"
                :key="substance.id"
                :label="substance.name"
                class="mx-1"
              ></DsfrTag>
            </div>
          </div>
          <!-- TODO: add max quantity, nutritional reference, unit for substance -->
          <p><i>Population cible et à risque en construction</i></p>
        </DsfrFieldset>
        <DsfrFieldset legend="Commentaire à destination du public" legendClass="fr-h4">
          <div class="flex">
            <DsfrInput label="Commentaire" v-model="state.publicComment" :isTextarea="true" />
            <div class="mt-2">
              <DsfrCheckbox
                v-model="state.copyPublicCommentToPrivate"
                name="copy-comment"
                label="Copier dans les notes internes"
              />
            </div>
          </div>
        </DsfrFieldset>
        <div class="flex gap-x-2 mt-4">
          <!-- Question: cancel button? -->
          <!-- Question: use DsfrButtonGroup? -->
          <DsfrButton label="Enregistrer ingrédient" @click="saveElement" :disabled="isFetching" />
          <!-- <DsfrButton label="Sauvegarder brouillon" @click="saveAsDraft" :disabled="isFetching" secondary /> -->
        </div>
      </FormWrapper>
    </div>
  </div>
</template>

<script setup>
import { ref, computed /*, watch*/ } from "vue"
import { getTypeIcon, getTypeInFrench, unSlugifyType /*, getApiType*/ } from "@/utils/mappings"
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

// const props = defineProps({ urlComponent: String })
// const elementId = computed(() => props.urlComponent.split("--")[0])
// const type = computed(() => unSlugifyType(props.urlComponent.split("--")[1]))
const type = ref("plant")
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
}) // TODO: prefill with existing data if modifying

const isFetching = false // TODO: set to true when fetching data or sending update, see CompanyForm

const saveElement = async () => {
  // TODO: validate form before anything else
  // TODO: map misc ingredient types to other-ingrediet with getApiType or whatever
  const url = `/api/v1/${type.value}s/`
  const payload = state.value
  if (payload.substances.length) {
    payload.substances = payload.substances.map((substance) => substance.id)
  }
  // TODO: this will need updating when modifying ingredients
  payload.synonyms = payload.synonyms.filter((s) => !!s.name)
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
// const saveAsDraft = async () => {}
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
    plantParts: true,
    substances: true,
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
    substances: true,
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

const substanceTypes = [] // TODO: fetch options from DB
const ingredientTypes = [] // TODO: fetch options from DB

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
