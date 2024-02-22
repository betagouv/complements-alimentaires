<template>
  <div class="fr-card fr-enlarge-link">
    <div class="fr-card__body">
      <div class="fr-card__content">
        <div class="fr-card__title" style="order: unset">
          <router-link :to="route" class="fr-card__link capitalize">{{ result.name }}</router-link>
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
import { getTypeIcon, getType } from "@/utils/mappings"

const props = defineProps({
  result: Object,
})
const icon = computed(() => getTypeIcon(props.result.objectType))
const type = computed(() => getType(props.result.objectType))
const route = computed(() => {
  const urlComponent = `${props.result?.id}--${type.value?.toLowerCase()}--${props.result?.name}`
  return { name: "ElementView", params: { urlComponent } }
})
</script>
