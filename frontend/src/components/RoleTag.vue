<template>
  <!-- on n'utilise pas directement le composant DsfrTag car il n'est pas assez personnalisable -->
  <div>
    <component
      :is="showActions ? 'button' : 'p'"
      class="flex items-center fr-badge fr-badge--new fr-badge--no-icon fr-badge--sm"
      :aria-label="showActions && `Retirer le rôle ${roleName} à ${user.firstName} ${user.lastName}`"
      @click="showActions && $emit('remove')"
    >
      <v-icon class="size-3.5" name="ri-user-settings-line" />
      <div class="ml-0.5">{{ roleName }}</div>
      <v-icon v-if="showActions" class="size-4 ml-1" name="ri-close-circle-line" />
    </component>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { roleNameDisplayNameMapping } from "@/utils/mappings"

const props = defineProps({ role: String, showActions: { type: Boolean, default: false }, user: Object })
defineEmits(["remove"])

const roleName = computed(() => roleNameDisplayNameMapping[props.role])
</script>
