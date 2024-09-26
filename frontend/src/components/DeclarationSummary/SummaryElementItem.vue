<template>
  <li class="border-l-2 border-b pl-4 py-2">
    <div class="flex content-center">
      <ElementCommentModal v-model="model" class="mr-2" />
      <div class="self-center">
        <p class="capitalize font-bold mb-0">
          {{ getElementName(model).toLowerCase() }}
        </p>
      </div>

      <DsfrBadge v-if="model.new" label="Nouvel ingrédient" type="info" class="self-center ml-2" small />
    </div>
    <p class="my-2">
      {{ elementInfo }}
    </p>
  </li>
</template>

<script setup>
import { computed } from "vue"
import { getElementName } from "@/utils/elements"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import ElementCommentModal from "@/components/ElementCommentModal"

const { plantParts, units, preparations } = storeToRefs(useRootStore())

const model = defineModel()
const props = defineProps({ objectType: { type: String } })

const plantPartName = computed(() => plantParts.value?.find((x) => x.id === model.value.usedPart)?.name || "Aucune")
const unitName = computed(() => units.value?.find((x) => x.id === model.value.unit)?.name || "")
const preparationName = computed(
  () => preparations.value?.find((x) => x.id === parseInt(model.value.preparation))?.name || ""
)

const elementInfo = computed(() => {
  if (props.objectType === "microorganism") {
    const strain_label = `Souche : « ${model.value.strain} »`
    const quantity_label = model.value.quantity ? `Qté par DJR (en UFC) : ${model.value.quantity}` : null
    return [strain_label, quantity_label].filter(Boolean).join(` | `)
  }
  if (props.objectType === "plant") {
    const used_part_label = `Partie utilisée : « ${plantPartName.value} »`
    const quantity_label = model.value.quantity ? `Qté par DJR : ${model.value.quantity} ${unitName.value}` : null
    const preparation_label = model.value.preparation ? `Préparation : ${preparationName.value}` : null
    return [used_part_label, quantity_label, preparation_label].filter(Boolean).join(` | `)
  }

  if (
    props.objectType === "form_of_supply" ||
    props.objectType === "active_ingredient" ||
    props.objectType === "substance"
  )
    return model.value.quantity ? `Qté par DJR: ${model.value.quantity} ${unitName.value}` : null
  return ""
})
</script>
