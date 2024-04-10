<template>
  <div class="flex mt-6 mb-3" v-if="elements.length">
    <div :class="`mr-4 self-center justify-center rounded-full icon icon-${objectType} size-8 flex`">
      <v-icon class="self-center" fill="white" :name="getTypeIcon(objectType)" />
    </div>
    <p class="m-0 font-bold capitalize self-center">{{ getType(objectType) }}s</p>
  </div>
  <TransitionGroup mode="out-in" name="list" tag="div" class="mt-2 relative">
    <ElementCard
      v-for="(element, index) in elements"
      :key="`${objectType}-${index}`"
      @remove="(elem) => $emit('remove', elem)"
      v-model="elements[index]"
      class="mb-2"
      :objectType="objectType"
    />
  </TransitionGroup>
</template>

<script setup>
import ElementCard from "./ElementCard.vue"
import { getTypeIcon, getType } from "@/utils/mappings"

defineProps({ objectType: { type: String }, elements: { type: Array } })
defineEmits(["remove"])
</script>
