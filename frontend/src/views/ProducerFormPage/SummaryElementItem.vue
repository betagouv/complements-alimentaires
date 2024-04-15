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

const model = defineModel()
const props = defineProps({ objectType: { type: String } })

const elementInfo = computed(() => {
  if (props.objectType === "microorganism")
    return `Souche : « ${model.value.strain} » | Qté par DJR (en CFU) : ${model.value.quantity}`
  if (props.objectType === "plant")
    return `Partie utilisée : « ${model.value.plantPart} » | Qté par DJR : ${model.value.quantity} ${model.value.unit || ""} | Préparation : ${model.value.preparation}`
  return ""
})
</script>
