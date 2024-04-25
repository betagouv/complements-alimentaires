<template>
  <!-- on n'utilise pas directement le composant DsfrTag car il n'est pas assez personnalisable -->
  <div class="flex items-center fr-badge fr-badge--new fr-badge--no-icon fr-badge--sm">
    <v-icon class="size-3" name="ri-user-3-line" />
    <div class="ml-0.5">{{ role.displayName }}</div>
    <v-icon
      v-if="props.showActions"
      class="size-4 ml-1 hover:text-red-marianne-425 hover:cursor-pointer"
      name="ri-close-circle-line"
    />
  </div>
</template>

<script setup>
const props = defineProps({ role: Object, showActions: { type: Boolean, default: false } })
</script>
