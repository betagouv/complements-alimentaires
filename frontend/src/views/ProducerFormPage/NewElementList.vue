<template>
  <TypeHeader :objectType="objectType" v-if="elements.length" />
  <NewElementCard
    :key="`new-${objectType}-${index}`"
    v-for="(_, index) in elements"
    v-model="elements[index]"
    :objectType="objectType"
  />
</template>

<script setup>
import NewElementCard from "./NewElementCard"
import TypeHeader from "./TypeHeader"
defineProps({ objectType: { type: String }, elements: { type: Array } })
</script>
