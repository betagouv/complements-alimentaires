<template>
  <li>
    <div class="capitalize">{{ name.toLowerCase() }}</div>
    <div class="mt-1">
      {{ elementInfo }}
    </div>
  </li>
</template>

<script setup>
import { computed } from "vue"

const model = defineModel()
const props = defineProps({ objectType: { type: String } })

const name = computed(
  () => model.value.element?.name || model.value.newName || `${model.value.newGenre} ${model.value.newSpecies}`
)

const elementInfo = computed(() => {
  if (props.objectType === "microorganism")
    return `Souche : « ${model.value.strain} » | Qté par DJR (en CFU) : ${model.value.cfu_quantity}`
  if (props.objectType === "plant")
    return `Partie utilisée : « ${model.value.plantPart} » | Qté par DJR : ${model.value.quantity} ${model.value.unit || ""} | Préparation : ${model.value.preparation}`
  return ""
})
</script>
