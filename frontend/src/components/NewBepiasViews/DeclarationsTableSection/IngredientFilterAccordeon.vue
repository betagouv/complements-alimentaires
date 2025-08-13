<template>
  <DsfrAccordionsGroup v-model="activeIngredientAccordion">
    <DsfrAccordion>
      <template v-slot:title>
        <p>
          <v-icon scale="0.85" class="mr-2" :name="icon" />
          {{ name }}
        </p>
      </template>
      <p>{{ modelValue }}</p>
    </DsfrAccordion>
  </DsfrAccordionsGroup>
</template>

<script setup>
import { computed, ref } from "vue"
import { typesMapping, getTypeIcon } from "@/utils/mappings"

const modelValue = defineModel()
const activeIngredientAccordion = ref(0)

const icon = computed(() => getTypeIcon(modelValue.value?.split("||")[0]))

const name = computed(() => {
  const parts = modelValue.value.split("||")
  const type = typesMapping[parts[0]] || "Ingrédient"
  const name = parts[1] || "Inconnu"
  return `${type} : ${name}`
})
</script>
