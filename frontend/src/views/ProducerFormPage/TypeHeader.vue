<template>
  <div class="flex mt-6 mb-3">
    <div :class="`mr-4 self-center justify-center rounded-full icon icon-${objectType} size-8 flex`">
      <v-icon class="self-center" fill="white" :name="getTypeIcon(objectType)" />
    </div>
    <h3 class="m-0 font-bold self-center fr-text--md">{{ typeName }}</h3>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { getTypeIcon, getTypeInFrench } from "@/utils/mappings"
const props = defineProps({ objectType: { type: String } })

const typeName = computed(() => {
  const typeNameInfo = getTypeInFrench(props.objectType)
  return typeNameInfo?.plural || `${typeNameInfo}s`
})
</script>
