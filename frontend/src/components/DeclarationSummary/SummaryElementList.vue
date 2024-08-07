<template>
  <div v-if="elements.length">
    <div class="flex mt-6 mb-3">
      <div :class="`mr-2 self-center justify-center rounded-full size-4 flex`">
        <v-icon class="self-center" :name="getTypeIcon(objectType)" />
      </div>
      <p class="m-0 font-bold capitalize self-center">{{ getTypeInFrench(objectType) }}s</p>
    </div>

    <ul class="list-none">
      <SummaryElementItem
        class="mb-2 last:mb-0"
        v-for="(element, index) in elements"
        :key="`summary-${objectType}-${index}`"
        v-model="elements[index]"
        :objectType="objectType"
      />
    </ul>
  </div>
</template>

<script setup>
import { getTypeIcon, getTypeInFrench } from "@/utils/mappings"
import SummaryElementItem from "./SummaryElementItem"

defineProps({ objectType: { type: String }, elements: { type: Array } })
</script>
