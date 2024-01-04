<template>
  <div class="fr-card fr-enlarge-link">
    <div class="fr-card__body">
      <div class="fr-card__content">
        <div class="fr-card__title" style="order: unset">
          <a href="#" class="fr-card__link">{{ result.name }}</a>
        </div>
        <div class="mt-2 flex">
          <div><v-icon scale="0.85" class="mr-1" :name="icon" /></div>
          <div style="margin-top: 1px">{{ type }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  result: Object,
})
const icon = computed(() => {
  const mapping = {
    plant: "ri-plant-line",
    microorganism: "ri-microscope-line",
    ingredient: "ri-flask-line",
    substance: "ri-test-tube-line",
  }
  return mapping[props.result.objectType] || null
})
const type = computed(() => {
  const mapping = {
    plant: "Plante",
    microorganism: "Micro-organism",
    ingredient: "Ingredient",
    substance: "Substance",
  }
  return mapping[props.result.objectType] || null
})
</script>
