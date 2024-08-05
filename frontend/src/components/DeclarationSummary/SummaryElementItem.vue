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

const { plantParts, units } = storeToRefs(useRootStore())

const model = defineModel()
const props = defineProps({ objectType: { type: String } })

const plantPartName = computed(() => plantParts.value?.find((x) => x.id === model.value.usedPart)?.name || "Aucune")
const unitName = computed(() => units.value?.find((x) => x.id === model.value.unit)?.name || "")

const elementInfo = computed(() => {
  if (props.objectType === "microorganism") {
    const strain_label = `Souche : « ${model.value.strain} »`
    const quantity_label = model.value.quantity ? `Qté par DJR (en UFC) : ${model.value.quantity}` : null
    return [strain_label, quantity_label].filter(Boolean).join(` | `)
  }
  if (props.objectType === "plant") {
    const used_part_label = `Partie utilisée : « ${plantPartName.value} »`
    const quantity_label = model.value.quantity ? `Qté par DJR : ${model.value.quantity} ${unitName.value}` : null
    const preparation_label = model.value.preparation ? `Préparation : ${model.value.preparation}` : null
    return [used_part_label, quantity_label, preparation_label].filter(Boolean).join(` | `)
  }
  if (props.objectType === "form_of_supply" || props.objectType === "active_ingredient")
    return model.value.quantity ? `Qté par DJR: ${model.value.quantity} ${unitName.value}` : ""
  return ""
})
</script>
