<template>
  <div class="col-span-12 sm:col-span-4 md:col-span-3 flex flex-col mt-4">
    <div class="fr-text--sm font-medium! mb-1!">{{ title }}</div>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  title: String,
})
</script>
