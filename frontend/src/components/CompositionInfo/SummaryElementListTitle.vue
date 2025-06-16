<template>
  <div class="flex">
    <div :class="`mr-2 self-center justify-center rounded-full size-4 flex`">
      <v-icon class="self-center" :name="getTypeIcon(objectType)" />
    </div>
    <p class="m-0 font-bold capitalize self-center">
      {{ getTypeInFrench(objectType) }}s
      <span v-if="elementCount">({{ elementCount }})</span>
    </p>
  </div>
</template>

<script setup>
import { getTypeIcon, getTypeInFrench } from "@/utils/mappings"

defineProps({ objectType: { type: String }, elementCount: { type: String, default: "" } })
</script>
