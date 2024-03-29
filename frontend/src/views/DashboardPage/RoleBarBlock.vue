<template>
  <DsfrNotice>
    <div class="flex items-center gap-x-2.5 gap-y-1 flex-wrap">
      <p class="shrink-0">Bienvenue, {{ name }}</p>
      <div class="flex gap-x-1.5">
        <DsfrTag
          v-for="role in roles"
          :key="role.name"
          :label="role.displayName"
          icon="ri-account-circle-line"
          class="flex gap-x-1 border border-gray-300 capitalize whitespace-nowrap"
          small
        />
      </div>
    </div>
  </DsfrNotice>
</template>

<script setup>
defineProps({ name: String, roles: Array })
</script>
