<template>
  <TypeHeader :objectType="objectType" v-if="elements.length" />
  <TransitionGroup mode="out-in" name="list" tag="div" class="mt-2 relative">
    <ElementCard
      v-for="(element, index) in elements"
      :key="`${objectType}-${index}`"
      @remove="(elem) => $emit('remove', elem)"
      v-model="elements[index]"
      class="mb-2"
      :objectType="objectType"
      :canAddNewPlantPart="true"
    />
  </TransitionGroup>
</template>

<script setup>
import ElementCard from "@/components/ElementCard"
import TypeHeader from "./TypeHeader"

defineProps({ objectType: { type: String }, elements: { type: Array } })
defineEmits(["remove"])
</script>
