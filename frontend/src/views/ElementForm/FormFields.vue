<template>
  <FormWrapper :externalResults="$externalResults" class="mx-auto">
    <DsfrFieldset legend="Identité de l’ingrédient" legendClass="fr-h4 !mb-0 !pb-2">
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-x-8">
        <div class="col-span-2 lg:col-span-4" v-if="formForType.name">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'name')">
            <DsfrInput v-model="state.name" :label="formForType.name.label" required labelVisible />
          </DsfrInputGroup>
        </div>
        <div v-if="formForType.species" class="col-span-2">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'species')">
            <DsfrInput v-model="state.species" label="Espèce du micro-organisme" labelVisible required />
          </DsfrInputGroup>
        </div>
        <div v-if="formForType.genus" class="col-span-2">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'genus')">
            <DsfrInput v-model="state.genus" label="Genre" labelVisible required />
          </DsfrInputGroup>
        </div>
        <div class="col-span-2">
          <DsfrInputGroup>
            <DsfrSelect v-model.number="state.status" label="Autorisation de l’ingrédient" :options="statuses" />
          </DsfrInputGroup>
        </div>
        <div class="col-span-2" v-if="formForType.family && plantFamiliesDisplay">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'family')">
            <DsfrSelect
              v-model.number="state.family"
              label="Famille de la plante"
              :options="plantFamiliesDisplay"
              labelKey="name"
              required
            />
          </DsfrInputGroup>
        </div>
        <div v-if="formForType.ingredientType" class="col-span-2">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'ingredientType')">
            <DsfrSelect
              v-model.number="state.ingredientType"
              label="Type de l'ingrédient"
              :options="ingredientTypes"
              required
            />
          </DsfrInputGroup>
        </div>

        <DsfrInputGroup v-if="formForType.einecNumber">
          <DsfrInput v-model="state.einecNumber" label="Numéro EINECS" labelVisible />
        </DsfrInputGroup>
        <DsfrInputGroup v-if="formForType.casNumber">
          <DsfrInput v-model="state.casNumber" label="Numéro CAS" labelVisible />
        </DsfrInputGroup>
        <DsfrToggleSwitch
          v-if="!state.ingredientType || state.ingredientType != aromaId"
          v-model="state.novelFood"
          label="Novel food"
          activeText="Oui"
          inactiveText="Non"
          label-left
          class="self-center mt-4 col-span-2 sm:col-span-1"
        />
        <DsfrToggleSwitch
          v-model="state.isRisky"
          label="Nécessite une instruction manuelle et vigilante ?"
          activeText="Oui"
          inactiveText="Non"
          label-left
          class="self-center mt-4 col-span-2 sm:col-span-2"
        />
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
            v-for="(id, idx) in state.plantParts"
            :key="`plant-part-${id}`"
            :label="optionLabel(plantParts, id)"
            tagName="button"
            @click="state.plantParts.splice(idx, 1)"
            :aria-label="`Retirer ${optionLabel(plantParts, id)}`"
            class="mx-1 fr-tag--dismiss"
          ></DsfrTag>
        </div>
      </div>
      <div v-if="formForType.substances" class="grid md:grid-cols-3 items-end my-4 md:my-2">
        <ElementAutocomplete
          autocomplete="nothing"
          label="Substances actives"
          label-visible
          class="max-w-md grow mb-3"
          hint="Tapez au moins trois caractères pour démarrer la recherche"
          :hideSearchButton="true"
          @selected="selectOption"
          type="substance"
          :required="false"
        />
        <div class="md:ml-4 md:my-7 md:col-span-2">
          <DsfrTag
            v-for="(substance, idx) in state.substances"
            :key="`substance-${substance.id}`"
            :label="substance.name"
            tagName="button"
            @click="state.substances.splice(idx, 1)"
            :aria-label="`Retirer ${substance.name}`"
            class="mx-1 fr-tag--dismiss"
          ></DsfrTag>
        </div>
      </div>
      <div class="grid grid-cols-3 gap-x-8" v-if="formForType.nutritionalReference">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'nutritionalReference')">
          <NumberField label="Apport nutritionnel de référence" label-visible v-model="state.nutritionalReference" />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'maxQuantity')">
          <NumberField label="Quantité maximale autorisée" label-visible v-model="state.maxQuantity" />
        </DsfrInputGroup>
        <div class="max-w-32">
          <DsfrInputGroup v-if="isNewIngredient" :error-message="firstErrorMsg(v$, 'unit')">
            <DsfrSelect
              label="Unité"
              label-visible
              :options="store.units?.map((unit) => ({ text: unit.name, value: unit.id }))"
              v-model="state.unit"
              defaultUnselectedText="Unité"
            />
          </DsfrInputGroup>
          <div v-else class="pt-4">
            <p class="mb-2">Unité</p>
            <p>{{ unitString }}</p>
          </div>
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
      <DsfrInputGroup v-if="!isNewIngredient" :error-message="firstErrorMsg(v$, 'changeReason')">
        <DsfrInput
          v-model="state.changeReason"
          label="Raison de changement (public)"
          hint="100 caractères max"
          required
          labelVisible
        />
      </DsfrInputGroup>
    </DsfrFieldset>
    <div class="flex gap-x-2 mt-4">
      <DsfrButton label="Enregistrer ingrédient" @click="saveElement" />
    </div>
  </FormWrapper>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { getApiType } from "@/utils/mappings"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import { handleError } from "@/utils/error-handling"
import { firstErrorMsg, errorRequiredField, errorNumeric, errorMaxStringLength } from "@/utils/forms"
import { getUnitString } from "@/utils/elements"
import { useVuelidate } from "@vuelidate/core"
import useToaster from "@/composables/use-toaster"
import FormWrapper from "@/components/FormWrapper"
import ElementAutocomplete from "@/components/ElementAutocomplete"
import NumberField from "@/components/NumberField"

const props = defineProps({ element: Object, type: String })

const isNewIngredient = computed(() => !props.element?.id)

const elementId = computed(() => props.element?.id)
const apiType = computed(() => props.type && getApiType(props.type))
const router = useRouter()

const createEmptySynonym = () => ({ name: "" })

const state = ref({
  plantParts: [],
  substances: [],
  synonyms: [createEmptySynonym(), createEmptySynonym(), createEmptySynonym()],
})

watch(
  () => props.element,
  () => {
    state.value = JSON.parse(JSON.stringify(props.element))
    state.value.status = statuses.find((s) => s.apiValue === state.value.status)?.value
    if (state.value.family) state.value.family = state.value.family.id
    if (state.value.plantParts) state.value.plantParts = state.value.plantParts.map((p) => p.id)
    if (state.value.objectType && apiType.value === "other-ingredient")
      state.value.ingredientType = ingredientTypes.find((t) => t.apiValue === state.value.objectType).value
    if (state.value.unitId) state.value.unit = state.value.unitId
  }
)

const saveElement = async () => {
  v$.value.$reset()
  v$.value.$validate()
  if (v$.value.$error) {
    window.scrollTo(0, 0)
    return
  }

  const url = `/api/v1/${apiType.value}s/`
  const payload = state.value
  if (payload.substances?.length) {
    payload.substances = payload.substances.map((substance) => substance.id)
  }
  payload.synonyms = payload.synonyms.filter((s) => !!s.name)
  if (payload.ingredientType && payload.ingredientType == aromaId) delete payload.novelFood

  const { response } = isNewIngredient.value
    ? await useFetch(url, { headers: headers() }).post(payload).json()
    : await useFetch(url + elementId.value, { headers: headers() })
        .patch(payload)
        .json()
  $externalResults.value = await handleError(response)

  if (response.value.ok) {
    useToaster().addMessage({
      type: "success",
      id: "element-creation-success",
      description: `L'ingrédient a été ${isNewIngredient.value ? "créé" : "modifié"}`,
    })
    if (isNewIngredient.value) router.push({ name: "DashboardPage" })
    else router.navigateBack({ name: "DashboardPage" })
  }
}
const addNewSynonym = async () => {
  state.value.synonyms.push(createEmptySynonym())
}

const formQuestions = {
  plant: {
    name: {
      label: "Nom de la plante",
    },
    family: true,
    function: true,
    // status: true for every type
    // novelFood is true for every type
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
  ingredient: {
    name: {
      label: "Nom ingrédient",
    },
    ingredientType: true,
    function: true,
    substances: true,
  },
}
const formForType = computed(() => {
  return formQuestions[props.type] || (!isNewIngredient.value && formQuestions.ingredient)
})
const rules = computed(() => {
  const form = formForType.value
  return {
    name: form?.name ? errorRequiredField : {},
    species: form?.species ? errorRequiredField : {},
    genus: form?.genus ? errorRequiredField : {},
    ingredientType: form?.ingredientType ? errorRequiredField : {},
    family: form?.family ? errorRequiredField : {},
    nutritionalReference: form?.nutritionalReference ? errorNumeric : {},
    maxQuantity: form?.maxQuantity ? errorNumeric : {},
    changeReason: isNewIngredient.value ? {} : Object.assign({}, errorRequiredField, errorMaxStringLength(100)),
  }
})
watch(formForType, () => v$.value.$reset())

const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

const store = useRootStore()
const { plantParts, plantFamilies, units } = storeToRefs(store)
store.fetchDeclarationFieldsData()
store.fetchPlantFamilies()

const ingredientTypes = [
  { value: 1, text: "Nutriment (Forme d'apport)", apiValue: "form_of_supply" },
  { value: 2, text: "Additif", apiValue: "additif" },
  { value: 3, text: "Arôme", apiValue: "aroma" },
  { value: 4, text: "Autre ingrédient actif", apiValue: "active_ingredient" },
  { value: 5, text: "Autre ingrédient", apiValue: "non_active_ingredient" },
]

const statuses = [
  { value: 1, text: "Autorisé", apiValue: "autorisé" },
  { value: 2, text: "Non autorisé", apiValue: "non autorisé" },
  { value: 3, text: "Sans objet", apiValue: "sans objet" },
]

const selectOption = async (result) => {
  state.value.substances.push(result)
}

const optionLabel = (options, id) => {
  return options?.find((o) => o.id === id)?.name || "Inconnu"
}

const plantFamiliesDisplay = computed(() => {
  return plantFamilies.value
    ?.map((family) => ({ value: family.id, text: family.name }))
    .sort((a, b) => a.text.localeCompare(b.text))
})

const aromaId = 3

const unitString = computed(() => {
  return getUnitString(state.value.unit, units)
})
</script>
