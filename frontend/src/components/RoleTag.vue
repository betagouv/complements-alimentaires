<template>
  <!-- on n'utilise pas directement le composant DsfrTag car il n'est pas assez personnalisable -->
  <div class="flex items-center fr-badge fr-badge--new fr-badge--no-icon fr-badge--sm">
    <v-icon class="size-3.5" name="ri-user-settings-line" />
    <div class="ml-0.5">{{ roleNameDisplayNameMapping[role] }}</div>
    <v-icon
      v-if="showActions"
      role="button"
      aria-label="Enlèver ce rôle"
      @click="$emit('remove')"
      class="size-4 ml-1 hover:text-red-marianne-425 hover:cursor-pointer"
      name="ri-close-circle-line"
    />
  </div>
</template>

<script setup>
import { roleNameDisplayNameMapping } from "@/utils/mappings"

defineProps({ role: String, showActions: { type: Boolean, default: false } })
defineEmits(["remove"])
</script>
