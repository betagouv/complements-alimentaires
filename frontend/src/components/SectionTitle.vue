<template>
  <component :is="headerTag" :class="`fr-${sizeTag} flex gap-x-2`">
    <v-icon class="mt-[4px]" v-if="icon" :name="icon" />
    {{ title }}
  </component>
</template>

<script setup>
defineProps({
  title: { type: String },
  icon: { type: String, default: undefined },
  headerTag: { type: String, default: "h2" },
  sizeTag: { type: String, default: "h5" },
})
</script>
