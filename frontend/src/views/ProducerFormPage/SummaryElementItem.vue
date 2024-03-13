<template>
  <li>
    <div class="capitalize font-bold">{{ props.element.element.name }}</div>
    <div class="mt-1">
      <v-icon class="self-center" :name="getTypeIcon(element.element.objectType)" />
      {{ elementInfo }}
    </div>
  </li>
</template>

<script setup>
import { computed } from "vue"
import { getTypeIcon, getType } from "@/utils/mappings"

const props = defineProps({ element: Object })

const elementInfo = computed(() => {
  const objectType = props.element.element.objectType
  const type = getType(objectType)
  if (objectType === "microorganism")
    return `${type} | Souche : « ${props.element.strain} » | Qté par DJR (en CFU) : ${props.element.cfu_quantity}`
  if (objectType === "plant")
    return `${type} | Partie utilisée : « ${props.element.plantPart} » | Qté par DJR : ${props.element.quantity} ${props.element.unit || ""} | Préparation : ${props.element.preparation}`
  return type
})
</script>
