<template>
  <DsfrTable ref="table" class="w-full" :headers="headers" :rows="rows" :no-caption="true" :pagination="false" />
</template>

<script setup>
import { computed, watch } from "vue"
import ElementCommentModal from "@/components/ElementCommentModal"
import QuantityInputCell from "./QuantityInputCell"

const payload = defineModel()
const props = defineProps({ readonly: Boolean, hidePrivateComments: Boolean })

const headers = ["", "Nom", "Ingrédient(s) source", "Qté totale par DJR", "Unité"]

const rows = computed(() => {
  return payload.value.computedSubstances.map((substance, index) => ({
    rowData: [
      {
        component: ElementCommentModal,
        hidePrivateComments: props.hidePrivateComments,
        modelValue: substance,
      },
      {
        component: "span",
        text: substance.substance.name.toLowerCase(),
        class: "capitalize",
      },
      {
        component: "span",
        text: sourceElements(substance.substance),
        class: "capitalize",
      },
      {
        component: QuantityInputCell,
        modelValue: payload.value,
        amountInfoText: amountInfoText.value[index],
        readonly: props.readonly,
        rowIndex: index,
      },
      payload.value.computedSubstances[index].substance.unit,
    ],
  }))
})

const elements = computed(() =>
  [].concat(
    payload.value.declaredPlants,
    payload.value.declaredMicroorganisms,
    payload.value.declaredIngredients,
    payload.value.declaredSubstances
    // Aromas et Additives ne sont pas actif et ne sont donc pas liés à des substances actives
  )
)
const activeElements = computed(() => elements.value.filter((x) => x.active && !x.new))

const getSources = (substance) =>
  activeElements.value.filter(
    (x) =>
      (x.element.objectType === "substance" && x.element.id === substance.id) ||
      x.element.substances?.map((item) => item.id).indexOf(substance.id) > -1
  )

const sourceElements = (substance) => {
  const sources = getSources(substance)
  return sources.map((x) => x.element.name).join(", ")
}

const amountInfoText = computed(() => {
  return payload.value.computedSubstances.map((x) => {
    if (x.quantity !== 0 && !x.quantity) return ""

    const sourceElements = getSources(x.substance) || []
    const substanceSourceElements = sourceElements.filter((x) => x.element.objectType === "substance")
    const substanceSourcesHaveQuantities = substanceSourceElements?.some((x) => x.quantity)

    if (!substanceSourcesHaveQuantities) return ""

    const sourceQuantitySum = substanceSourceElements.reduce((acc, obj) => acc + (obj.quantity || 0), 0)
    if (x.quantity < sourceQuantitySum) {
      return `La quantité est inférieure à celle indiquée dans la composition (${sourceQuantitySum} ${x.substance.unit})`
    }
    return ""
  })
})

watch(
  elements,
  () => {
    const newSubstances = activeElements.value
      .map((x) => (x.element.objectType === "substance" ? [x.element] : x.element.substances))
      .flat()
      .filter((x) => !!x)

    // Ajouter les nouvelles substances
    newSubstances.forEach((newSubstance) => {
      if (!payload.value.computedSubstances.find((x) => x.substance.id === newSubstance.id))
        payload.value.computedSubstances.push({ substance: newSubstance, unit: newSubstance.unitId })
    })

    // Enlever les substances disparues
    payload.value.computedSubstances = payload.value.computedSubstances.filter((item) =>
      newSubstances.find((x) => x.id === item.substance.id)
    )
  },
  { deep: true, immediate: true }
)
</script>

<style scoped>
@reference "../../styles/index.css";

.fr-table :deep(table) {
  @apply table!;
}
.fr-table :deep(td) {
  @apply py-2;
}
.fr-table :deep(.fr-input-group) {
  @apply mt-0;
}
/* Colonne commentaire */
.fr-table :deep(td:nth-child(1)) {
  @apply w-16;
}
/* Colonne ingrédients source */
.fr-table :deep(td:nth-child(3)) {
  @apply max-w-16;
}
/* Colonne input quantité */
.fr-table :deep(td:nth-child(4)) {
  @apply max-w-48;
}
</style>
