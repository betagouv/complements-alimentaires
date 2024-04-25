<template>
  <!-- on n'utilise pas directement le composant DsfrTag car il n'est pas assez personnalisable -->
  <div class="flex items-center fr-badge fr-badge--warning fr-badge--no-icon fr-badge--sm">
    <v-icon class="size-3" name="ri-home-4-line" />
    <div class="ml-0.5">{{ name }}</div>
  </div>
</template>

<script setup>
defineProps({ name: String })
</script>
