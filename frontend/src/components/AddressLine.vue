<template>
  <address>
    {{ payload.address }}
    {{ payload.additional_details }}
    {{ payload.postal_code }}
    {{ payload.city }}
    {{ payload.country }}
    <span v-if="payload.cedex">- CEDEX : {{ payload.cedex }}</span>
  </address>
</template>

<script setup>
defineProps(["payload"])
</script>
