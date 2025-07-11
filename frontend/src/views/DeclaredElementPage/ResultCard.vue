<template>
  <DsfrCard
    class="capitalize"
    :link="route"
    :title="result.name"
    :endDetail="synonyms"
    :description="result.description"
  >
    <template #start-details>
      <div class="flex gap-x-2">
        <DsfrBadge v-if="result.isNovelFood" label="Novel Food" small type="new" />
        <ElementStatusBadge v-if="result.status" :text="result.status" />
      </div>
      <div class="my-2 flex gap-x-1">
        <div><v-icon scale="0.85" :name="icon" /></div>
        <div class="mt-px">{{ frenchType }}</div>
      </div>
    </template>
  </DsfrCard>
</template>

<script setup>
import { computed } from "vue"
import { getTypeIcon, getTypeInFrench } from "@/utils/mappings"
import { getElementUrlComponent } from "@/utils/elements"
import ElementStatusBadge from "@/components/ElementStatusBadge.vue"

const props = defineProps({
  result: Object,
})

const icon = computed(() => getTypeIcon(props.result.objectType))
const frenchType = computed(() => getTypeInFrench(props.result.objectType))

const route = computed(() => {
  if (!props.result) return
  return { name: "ElementPage", params: { urlComponent: getElementUrlComponent(props.result) } }
})

const synonyms = computed(() => {
  return props.result?.synonyms?.map((s) => s.name).join(", ")
})
</script>
