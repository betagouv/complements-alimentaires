<template>
  <span class="flex">
    <span :class="`mr-2 self-center justify-center rounded-full size-4 flex`">
      <v-icon class="self-center" :name="getTypeIcon(objectType)" />
    </span>
    <span class="m-0 capitalize font-bold self-center">
      {{ getTypeInFrench(objectType) }}s
      <span v-if="elementCount">({{ elementCount }})</span>
    </span>
  </span>
</template>

<script setup>
import { getTypeIcon, getTypeInFrench } from "@/utils/mappings"

defineProps({ objectType: { type: String }, elementCount: { type: String, default: "" } })
</script>
