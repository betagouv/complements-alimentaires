<template>
  <div class="bg-blue-france-950 h-14 flex items-center">
    <div class="fr-container">
      <div class="flex items-center gap-x-2.5 gap-y-1 flex-wrap">
        <div class="flex items-center gap-x-1">
          <v-icon class="text-blue-france-sun-113" name="ri-account-circle-line" />
          <div class="shrink-0 fr-notice__title text-blue-france-sun-113">Bienvenue, {{ name }}</div>
        </div>
        <div class="flex gap-x-1.5">
          <DsfrTag
            v-for="role in roles"
            :key="role.name"
            :label="role.displayName"
            icon="ri-file-user-line"
            class="flex gap-x-1 border border-gray-300 whitespace-nowrap"
            small
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ name: String, roles: Array })
</script>
