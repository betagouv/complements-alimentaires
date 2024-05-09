<template>
  <div class="flex mt-6 mb-3">
    <div :class="`mr-4 self-center justify-center rounded-full icon icon-${objectType} size-8 flex`">
      <v-icon class="self-center" fill="white" :name="getTypeIcon(objectType)" />
    </div>
    <p class="m-0 font-bold capitalize self-center">{{ getTypeInFrench(objectType) }}s</p>
  </div>
</template>

<script setup>
import { getTypeIcon, getTypeInFrench } from "@/utils/mappings"
defineProps({ objectType: { type: String } })
</script>
