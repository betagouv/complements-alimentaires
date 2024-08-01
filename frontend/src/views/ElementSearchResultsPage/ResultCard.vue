<template>
  <DsfrCard class="capitalize" :link="route" :title="result.name">
    <template #start-details>
      <ElementStatusBadge v-if="result.status" :text="result.status" />
      <div class="mt-2 flex gap-x-1">
        <div><v-icon scale="0.85" :name="icon" /></div>
        <div class="mt-[1px]">{{ frenchType }}</div>
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
