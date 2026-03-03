<template>
  <div class="col-span-12 sm:col-span-4 md:col-span-3 flex flex-col mt-4">
    <h2 class="fr-text--sm font-medium! mb-1!">{{ title }}</h2>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  title: String,
})
</script>
