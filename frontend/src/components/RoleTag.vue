<template>
  <DsfrBadge :label="role.displayName" type="new" noIcon small />
</template>

<script setup>
defineProps({ role: Object })
</script>
