<template>
  <div>
    <DsfrAlert
      v-if="externalResults && 'non_field' in externalResults"
      :description="externalResults.non_field"
      type="error"
      :small="true"
      class="mb-2"
    />
    <slot />
  </div>
</template>

<script setup>
defineProps({ externalResults: Object })
</script>
