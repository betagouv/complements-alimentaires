<template>
  <div class="fr-card fr-enlarge-link">
    <div class="fr-card__body">
      <div class="fr-card__content">
        <div class="fr-card__title" style="order: unset">
          <a :href="url" class="fr-card__link">{{ result.name }}</a>
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
import { useRouter } from "vue-router"
import { getTypeIcon } from "@/utils"

const router = useRouter()

const props = defineProps({
  result: Object,
})
const icon = computed(() => getTypeIcon(props.result.objectType))
const type = computed(() => {
  const mapping = {
    plant: "Plante",
    microorganism: "Micro-organisme",
    ingredient: "Ingredient",
    substance: "Substance",
  }
  return mapping[props.result.objectType] || null
})
const url = computed(() => {
  const urlComponent = `${props.result?.id}--${type.value?.toLowerCase()}--${props.result?.name}`
  return router.resolve({ name: "ElementView", params: { urlComponent } }).path
})
</script>
