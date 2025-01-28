<template>
  <div v-if="text">
    <h2 class="fr-h6 mb-1!">{{ title }}</h2>
    <p>
      <slot>{{ text }}</slot>
    </p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  text: String,
})
</script>
