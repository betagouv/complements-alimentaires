<template>
  <DsfrAccordionsGroup v-model="activeIngredientAccordion">
    <DsfrAccordion>
      <template v-slot:title>
        <p>
          <v-icon scale="0.85" class="mr-2" :name="icon" />
          {{ name }}
        </p>
      </template>

      <!-- Champs lors qu'il n'y a pas de dose spécifiée -->
      <div class="flex gap-4 items-end" v-if="!hasDoseFilter">
        <DsfrSelect v-if="isPlant" label="Partie de plante" v-model="selectedPart" :options="plantPartOptions" />
        <div>
          <DsfrButton @click="enableDoseFilter" label="Ajouter une dose" icon="ri-add-line" tertiary />
        </div>
      </div>

      <!-- Champs lors qu'on veut spécifier une dose -->
      <div v-else class="grid grid-cols-12 gap-4 items-center">
        <div class="col-span-12 md:col-span-3">
          <DsfrSelect v-if="isPlant" label="Partie de plante" v-model="selectedPart" :options="plantPartOptions" />
        </div>
        <div class="col-span-12 md:col-span-3">
          <DsfrSelect label="Opération" v-model="operation" :options="operationOptions" />
        </div>
        <div class="col-span-12 md:col-span-2">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'quantityA')">
            <NumberField :label="quantityALabel" v-model="quantityA" label-visible :required="true" />
          </DsfrInputGroup>
        </div>
        <div class="col-span-12 md:col-span-2" v-if="showDoubleQuantity">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'quantityB')">
            <NumberField :label="quantityBLabel" v-model="quantityB" label-visible :required="true" />
          </DsfrInputGroup>
        </div>
        <div class="col-span-12 md:col-span-2">
          <DsfrSelect v-model="unit" :options="unitOptions" label="Unité de mesure" />
        </div>
      </div>
    </DsfrAccordion>
  </DsfrAccordionsGroup>
</template>

<script setup>
import NumberField from "@/components/NumberField"
import { computed, ref, watch } from "vue"
import { typesMapping, getTypeIcon } from "@/utils/mappings"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { firstErrorMsg, errorNumeric } from "@/utils/forms"
import { useVuelidate } from "@vuelidate/core"
import { required, helpers } from "@vuelidate/validators"
import { OPERATION, operationOptions } from "@/utils/mappings.js"

const modelValue = defineModel()
const emit = defineEmits(["update:modelValue"])
const { units, plantParts } = storeToRefs(useRootStore())
const activeIngredientAccordion = ref(0)

const objectType = computed(() => modelValue.value.split("||")[0])
const isPlant = computed(() => objectType?.value === "plant")
const isMicroorganism = computed(() => objectType?.value === "microorganism")
const isSubstance = computed(() => objectType?.value === "substance")

// Valeurs initiales
const selectedPart = ref((isPlant.value && modelValue.value?.split("||")[2].split("|")[1]) || "")
const operation = ref(modelValue.value?.split("||")[3] || OPERATION.GT)

const extractQuantityA = () => {
  const rawValue = modelValue.value?.split?.("||")?.[4]?.split?.("|")[0]
  return rawValue ? parseInt(rawValue) : 0
}
const quantityA = ref(extractQuantityA())

const extractQuantityB = () => {
  const rawValues = modelValue.value?.split?.("||")?.[4]?.split?.("|")
  return rawValues.length > 0 ? parseInt(rawValues[1]) : 1
}
const quantityB = ref(extractQuantityB())

const extractUnit = () => {
  const segments = modelValue.value?.split("||")
  if (!segments || segments.length < 6) return null
  return segments[5]
}
const unit = ref(extractUnit())

// Parsing du modèle (qui est un String de filtre dose) et autres utils

const ingredientName = computed(() => modelValue.value.split("||")[1])
const ingredientId = computed(() => modelValue.value.split("||")[2].split("|")[0])
const icon = computed(() => getTypeIcon(objectType.value))
const name = computed(() => `${typesMapping[objectType] || "Ingrédient"} : ${ingredientName.value || "Inconnu"}`)

// Utils du formulaire
const makeQuantityLabel = (suffix) => {
  let label = operation.value === OPERATION.BT ? "Qté" : "Quantité"
  if (operation.value === OPERATION.BT) label += ` ${suffix}`
  if (isMicroorganism.value) label += " (en UFC)"
  if (isSubstance.value) label += ` (en ${units.value?.find((x) => x.id === parseInt(unit.value))?.name})`

  return label
}
const showDoubleQuantity = computed(() => operation.value === OPERATION.BT)
const quantityALabel = computed(() => makeQuantityLabel("min"))
const quantityBLabel = computed(() => makeQuantityLabel("max"))

const plantPartOptions = computed(() => {
  const options = plantParts.value?.map((x) => ({ text: x.name, value: x.id.toString() })) || []
  options.unshift({ disabled: true, text: "---------" })
  options.unshift({ value: "", text: "Toutes les parties" })
  return options
})
const unitOptions = computed(() => units.value?.map((x) => ({ text: x.name, value: x.id.toString() })))

// Validation du formulaire
const state = { quantityA, quantityB }
const rules = computed(() => ({
  quantityA: { required, errorNumeric },
  quantityB: showDoubleQuantity.value
    ? {
        required,
        errorNumeric,
        minValue: helpers.withMessage("La valeur doit être supérieur à la qté min", (value) => value > quantityA.value),
      }
    : {},
}))
const v$ = useVuelidate(rules, state)

// Mise à jour du modèle

const updateFilterString = () => {
  v$.value.$validate()
  if (v$.value.$error) return

  const commonInitialSection = `${objectType.value}||${ingredientName.value}||${ingredientId.value}`
  const midSection = isPlant.value
    ? `|${selectedPart.value || "-"}|${plantParts.value.find((x) => x.id.toString() === selectedPart.value)?.name || "Toutes les parties"}`
    : ""
  const endSection = `||${operation.value}||${quantityA.value}${showDoubleQuantity.value ? "|" + quantityB.value : ""}||${unit.value || ""}`
  emit("update:modelValue", `${commonInitialSection}${midSection}${endSection}`)
}
watch([selectedPart, quantityA, quantityB, unit, operation], updateFilterString)

// À noter : on considère que s'il y a une unité le filtre dose est actif
const hasDoseFilter = computed(() => operation.value && unit.value)
const enableDoseFilter = () => (unit.value = unitOptions.value?.[0]?.value || "")
</script>

<style scoped>
@reference "../../../styles/index.css";
div :deep(.fr-input-group) {
  @apply -mt-2!;
}
</style>
