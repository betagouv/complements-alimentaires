<template>
  <li>
    <div class="capitalize">{{ getElementName(model).toLowerCase() }}</div>
    <div class="mt-1">
      {{ elementInfo }}
    </div>
  </li>
</template>

<script setup>
import { computed } from "vue"
import { getElementName } from "@/utils/elements"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"

const { plantParts } = storeToRefs(useRootStore())

const model = defineModel()
const props = defineProps({ objectType: { type: String } })

const plantPartName = computed(() => plantParts.value?.find((x) => x.id === model.value.usedPart)?.name || "Aucune")

const elementInfo = computed(() => {
  if (props.objectType === "microorganism")
    return `Souche : « ${model.value.strain} » | Qté par DJR (en CFU) : ${model.value.quantity}`
  if (props.objectType === "plant")
    return `Partie utilisée : « ${plantPartName.value} » | Qté par DJR : ${model.value.quantity} ${model.value.unit || ""} | Préparation : ${model.value.preparation}`
  return ""
})
</script>
