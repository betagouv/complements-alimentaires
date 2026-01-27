<template>
  <a :href="href" target="_blank" rel="noopener external" :title="`${text || href} - nouvelle fenêtre`" class="fr-link">
    {{ text || href }}
  </a>
</template>

<script setup>
defineProps({ href: String, text: String })
</script>
