<template>
  <DsfrCard class="capitalize" :link="route" :title="result.name">
    <template #start-details>
      <div class="flex gap-x-2">
        <DsfrBadge v-if="result.novelFood" label="Novel Food" small type="new" />
        <ElementStatusBadge v-if="result.status" :text="result.status" />
      </div>
      <div class="mt-2 flex gap-x-1">
        <div><v-icon scale="0.85" :name="icon" /></div>
        <div class="mt-px">{{ frenchType }}</div>
      </div>
      <div class="italic" v-if="result.match && result.match !== result.name">
        {{ result.match }}
      </div>
    </template>
  </DsfrCard>
</template>

<script setup>
import { computed } from "vue"
import { getTypeIcon, getTypeInFrench, slugifyType } from "@/utils/mappings"
import ElementStatusBadge from "@/components/ElementStatusBadge.vue"

const props = defineProps({
  result: Object,
})
const icon = computed(() => getTypeIcon(props.result.objectType))
const frenchType = computed(() => getTypeInFrench(props.result.objectType))
const route = computed(() => {
  const urlComponent = `${props.result?.id}--${slugifyType(props.result.objectType)}--${props.result?.name}`
  return { name: "ElementPage", params: { urlComponent } }
})
</script>
