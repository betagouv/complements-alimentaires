<template>
  <span>
    «
    <router-link
      :to="{ name: 'DeclaredElementPage', params: { type: element.type, id: element.id } }"
      class="text-blue-france-sun-113"
    >
      {{ element.newName || element.element?.name }}
    </router-link>
    »
  </span>
</template>

<script setup>
defineProps({ element: Object })
</script>
