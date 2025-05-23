<template>
  <div v-if="modelStringIsValid">
    <DsfrModal size="lg" title="Filtrer par dose" :opened="opened" @close="removeFilter" :actions="modalActions">
      <div class="min-h-96">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'selectedIngredient')">
          <ElementAutocomplete
            v-model="ingredientSearchTerm"
            label="Ingrédient"
            label-visible
            class="md:w-3/4"
            hint="Cherchez l'ingrédient pour lequel vous souhaitez filtrer par dose."
            @selected="addIngredient"
            :hideSearchButton="true"
            :chooseFirstAsDefault="false"
            :searchAll="true"
          />
        </DsfrInputGroup>
        <div v-if="selectedIngredient">
          <DsfrAlert
            small
            type="warning"
            v-if="showMultipleSubstanceWarning"
            description="Cet ingrédient contient plusieurs substances. Les résultats contiendront les déclarations où au moins une substance correspond à la condition chosie."
          />
          <DsfrAlert
            small
            type="warning"
            v-else-if="showDoseMissingWarning"
            description="Les additifs, arômes et autres ingrédients non-actifs n'ont pas forcément de dose renseigné dans les déclarations. Vous pouvez néanmoins filtrer par composition."
          />
          <hr class="mt-2 pb-2" />
          <div class="md:flex gap-4 mt-4 mb-8 items-end">
            <div class="md:w-2/4 flex border items-center rounded p-2">
              <div
                :class="`flex mr-2 self-center justify-center rounded-full icon icon-${selectedIngredient.objectType} size-6`"
              >
                <v-icon
                  fill="white"
                  class="self-center"
                  :name="getTypeIcon(selectedIngredient.objectType)"
                  scale="0.8"
                ></v-icon>
              </div>
              <div>
                <p class="mb-0! fr-text--sm font-bold">
                  {{ selectedIngredient.name }}
                </p>
                <p class="mb-0! fr-text--sm italic">{{ getTypeInFrench(selectedIngredient.objectType) }}</p>
              </div>
            </div>
            <div>
              <DsfrSelect
                v-if="ingredientIsPlant"
                label="Partie de plante"
                v-model="selectedPart"
                :options="plantPartOptions"
              />
            </div>
          </div>
          <div class="md:flex gap-4">
            <div class="md:w-4/12">
              <DsfrInputGroup :error-message="firstErrorMsg(v$, 'selectedOperation')">
                <DsfrSelect
                  label="Opération"
                  :options="operationOptions"
                  v-model="selectedOperation"
                  defaultUnselectedText=""
                  :required="true"
                />
              </DsfrInputGroup>
            </div>
            <div class="mb-4 md:w-3/12">
              <DsfrInputGroup :error-message="firstErrorMsg(v$, 'selectedQuantity')">
                <NumberField :label="quantityALabel" v-model="selectedQuantity" label-visible :required="true" />
              </DsfrInputGroup>
            </div>
            <div class="mb-4 md:w-3/12" v-if="showDoubleQuantity">
              <DsfrInputGroup :error-message="firstErrorMsg(v$, 'selectedUpperLimitQuantity')">
                <NumberField
                  :label="quantityBLabel"
                  v-model="selectedUpperLimitQuantity"
                  label-visible
                  :required="true"
                />
              </DsfrInputGroup>
            </div>
            <div class="md:w-2/12" v-if="!ingredientIsMicroorganism && !ingredientIsSubstance">
              <DsfrInputGroup :error-message="firstErrorMsg(v$, 'selectedUnit')">
                <DsfrSelect
                  label="Unité"
                  :options="unitOptions"
                  v-model="selectedUnit"
                  defaultUnselectedText=""
                  :required="true"
                />
              </DsfrInputGroup>
            </div>
          </div>
        </div>
      </div>
    </DsfrModal>
    <div class="flex mt-2 mb-4" v-if="filterString">
      <v-icon class="self-center mr-3" :name="getTypeIcon(filterString.split('||')[0])"></v-icon>
      <div>
        <p class="mb-0 font-medium" v-for="line in filterTextLines" :key="`line-${line}`">{{ line }}</p>
      </div>
    </div>
    <p class="mb-2 italic" v-else>Aucun filtrage par dose n'est appliqué.</p>
    <DsfrButton
      tertiary
      @click="opened = true"
      size="small"
      v-if="!filterString"
      icon="ri-add-line"
      label="Ajouter un filtre dose"
    />
    <DsfrButton
      tertiary
      @click="removeFilter"
      size="small"
      v-else
      icon="ri-delete-bin-line"
      label="Supprimer le filtre dose"
    />
  </div>
</template>

<script setup>
/*
Le String résultant codifie le filtre par dose.
"<type d'élément>||<nom de l'élément>||<ID de l'élément (partie de plante optionnelle)>||<opération>||<quantité>||<ID de l'unité>"

« opération » peut être : >, ≥, <, ≤, =, ≬

Dans le cas des plantes, le string change pour inclure la partie de plante (facultative):
"plant||Camomille||<ID de la plante>|<ID de la partie>|<nom de la partie>||<opération>||<quantité>||<ID de l'unité>"

Dans le cas de l'opération "entre a et b" (≬), les deux quantités sont séparés de |
"<type d'élément>||<nom de l'élément>||<ID de l'élément>||≬||<quantité A>|<quantité B>||<ID de l'unité>"
*/
import NumberField from "@/components/NumberField"
import { ref, computed, onMounted, nextTick } from "vue"
import ElementAutocomplete from "@/components/ElementAutocomplete.vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { getTypeIcon, getTypeInFrench, typesMapping, getApiType } from "@/utils/mappings"
import { useVuelidate } from "@vuelidate/core"
import { required, helpers } from "@vuelidate/validators"
import { firstErrorMsg, errorNumeric } from "@/utils/forms"
import { useFetch } from "@vueuse/core"

const OPERATION = { GT: ">", GTE: "≥", LT: "<", LTE: "≤", EQ: "=", BT: "≬" }
const { units, plantParts } = storeToRefs(useRootStore())

const filterString = defineModel()

const ingredientSearchTerm = ref("")

const selectedIngredient = ref("")
const selectedPart = ref("") // Utilisé seulement dans le cas des plantes
const selectedOperation = ref("")
const selectedQuantity = ref("")
const selectedUpperLimitQuantity = ref("") // Utilisé seulement dans l'opération ≬ "entre a et b"
const selectedUnit = ref("")

const ingredientIsPlant = computed(() => selectedIngredient.value?.objectType === "plant")
const ingredientIsMicroorganism = computed(() => selectedIngredient.value?.objectType === "microorganism")
const ingredientIsSubstance = computed(() => selectedIngredient.value?.objectType === "substance")

const addIngredient = async (ingredient) => {
  selectedIngredient.value = ingredient
  if (!ingredientIsPlant.value) selectedPart.value = null
  if (ingredientIsSubstance.value) selectedUnit.value = selectedIngredient.value.unit
  if (
    selectedIngredient.value?.objectType === "form_of_supply" ||
    selectedIngredient.value?.objectType === "active_ingredient"
  ) {
    const url = `/api/v1/${getApiType(selectedIngredient.value?.objectType)}s/${selectedIngredient.value.id}`
    const { data } = await useFetch(url, { immediate: true }).get().json()
    selectedIngredient.value.substances = data.value?.substances
  }
}

const showDoubleQuantity = computed(() => selectedOperation.value === OPERATION.BT)
const quantityALabel = computed(() => makeQuantityLabel("min"))
const quantityBLabel = computed(() => makeQuantityLabel("max"))

const makeQuantityLabel = (suffix) => {
  let label = selectedOperation.value === OPERATION.BT ? "Qté" : "Quantité"
  if (selectedOperation.value === OPERATION.BT) label += ` ${suffix}`
  if (ingredientIsMicroorganism.value) label += " (en UFC)"
  if (ingredientIsSubstance.value)
    label += ` (en ${units.value?.find((x) => x.id === parseInt(selectedUnit.value))?.name})`

  return label
}

// Options pour les DsfrSelect
const plantPartOptions = computed(() => {
  const options = plantParts.value?.map((x) => ({ text: x.name, value: x.id.toString() }))
  options.unshift({ disabled: true, text: "---------" })
  options.unshift({ value: "", text: "Toutes les parties" })
  return options
})
const unitOptions = computed(() => units.value?.map((x) => ({ text: x.name, value: x.id.toString() })))
const operationOptions = [
  { text: "Dose supérieure à (>)", value: OPERATION.GT },
  { text: "Dose supérieure ou égale à (≥)", value: OPERATION.GTE },
  { text: "Dose inférieure à (<)", value: OPERATION.LT },
  { text: "Dose inférieure ou égale à (≤)", value: OPERATION.LTE },
  { text: "Dose égale à (=)", value: OPERATION.EQ },
  { text: "Dose entre deux valeurs", value: OPERATION.BT },
]

// Gestion du filtre

// Cette fonction rend le texte en français qui décrit en une ligne la dose appliquée
const filterTextLines = computed(() => {
  if (!modelStringIsValid.value) return []
  const [elementType, elementName, elementInfo, operation, quantities, unitId] = filterString.value?.split("||") || []
  const [quantityA, quantityB] = quantities.split("|")

  let unitName = ""
  if (unitId) unitName = units.value?.find((x) => x.id === parseInt(unitId))?.name
  else if (elementType === "microorganism") unitName = "UFC"
  const operationName =
    operation === OPERATION.BT
      ? `Dose entre ${quantityA} et ${quantityB}`
      : `${operationOptions.find((x) => x.value === operation)?.text} ${quantityA}`

  let typeName = getTypeInFrench(elementType).toLowerCase()
  if (elementType === "plant") {
    const [, partId, partName] = elementInfo.split("|")
    if (partId === "-") typeName += ` - ${partName.toLowerCase()}`
    else if (partId) typeName += ` - partie « ${partName.toLowerCase()} »`
  }

  // Exemple de résultat : ["Carex arenaria L. (plante - toutes les parties)", "Dose supérieure à (>) 12 mv"]
  return [`${elementName} (${typeName})`, `${operationName} ${unitName}`]
})

const setFilter = () => {
  v$.value.$validate()
  if (v$.value.$error) return

  // "<type d'élément>||<nom de l'élément>||<ID de l'élément (partie de plante optionnelle)>||<opération>||<quantité>||<ID de l'unité>"
  // "plant||Camomille||<ID de la plante>|<ID de la partie>|<nom de la partie>||<opération>||<quantité>||<ID de l'unité>"
  let newFilterString = `${selectedIngredient.value.objectType}||${selectedIngredient.value.name}||${selectedIngredient.value.id}`

  // Ajout de l'info sur la partie de plante en cas de ingrédient plante
  if (ingredientIsPlant.value) {
    const part = selectedPart.value
    newFilterString += `|${part ? part : "-"}|${part ? plantParts.value?.find((x) => x.id === parseInt(part))?.name : "Toutes les parties"}`
  }
  newFilterString += `||${selectedOperation.value}||${selectedQuantity.value}`

  // Ajout de la quantité maximale si l'opération est "entre a et b"
  if (selectedOperation.value === OPERATION.BT) newFilterString += `|${selectedUpperLimitQuantity.value}`

  if (selectedUnit.value) newFilterString += `||${selectedUnit.value}`

  filterString.value = newFilterString
  opened.value = false
}

const removeFilter = () => {
  const fieldsToReset = [
    ingredientSearchTerm,
    selectedIngredient,
    selectedPart,
    selectedOperation,
    selectedQuantity,
    selectedUpperLimitQuantity,
    selectedUnit,
  ]
  fieldsToReset.forEach((x) => (x.value = ""))
  filterString.value = ""
  v$.value.$reset()
  opened.value = false
}

// Gestion de la modale
const opened = ref(false)
const modalActions = [
  {
    label: "Confirmer",
    onClick: setFilter,
  },
  {
    label: "Annuler",
    secondary: true,
    onClick: removeFilter,
  },
]

// Validation du formulaire
const rules = computed(() => ({
  selectedIngredient: {
    required: helpers.withMessage("Merci de séléctionner un ingrédient pour filtrer la dose", required),
  },
  selectedOperation: { required },
  selectedQuantity: { required, errorNumeric },
  selectedUpperLimitQuantity:
    selectedOperation.value === OPERATION.BT
      ? {
          required,
          errorNumeric,
          minValue: helpers.withMessage(
            "La valeur doit être supérieur à la quantité A",
            (value) => value > selectedQuantity.value
          ),
        }
      : {},
  selectedUnit: ingredientIsMicroorganism.value ? {} : { required },
}))
const state = {
  selectedIngredient,
  selectedOperation,
  selectedQuantity,
  selectedUpperLimitQuantity,
  selectedUnit,
}
const v$ = useVuelidate(rules, state)

// Vérification basique du filterString : Smoke test pour éviter les coquilles le plus flagrantes dans les query params
const modelStringIsValid = computed(() => {
  if (!filterString.value) return true
  const [elementType, elementName, elementInfo, operation, quantities, unitId] = filterString.value.split("||") || []
  if (
    !elementType ||
    !elementName ||
    !elementInfo ||
    !operation ||
    !quantities ||
    (elementType !== "microorganism" && !unitId)
  )
    return false
  else if (!(elementType in typesMapping)) return false
  else if (Object.values(OPERATION).indexOf(operation) === -1) return false
  else if (elementType === "plant") {
    const [, , partName] = elementInfo.split("|")
    if (!partName) return false
  }
  if (operation === OPERATION.BT) {
    const [, quantityB] = quantities.split("|")
    if (!quantityB) return false
  }
  return true
})

// Alertes en cas de recherche par dose des ingrédients
const showMultipleSubstanceWarning = computed(() => {
  const objectType = selectedIngredient.value?.objectType
  if (objectType !== "form_of_supply" && objectType !== "active_ingredient") return false
  return selectedIngredient.value.substances?.length >= 2
})

const showDoseMissingWarning = computed(() => {
  const ingredientTypes = ["additive", "aroma", "non_active_ingredient"]
  return ingredientTypes.indexOf(selectedIngredient.value?.objectType) > -1
})

onMounted(() => {
  if (!modelStringIsValid.value) return nextTick(removeFilter)
})
</script>
