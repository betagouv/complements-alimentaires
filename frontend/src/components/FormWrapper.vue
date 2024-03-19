<template>
  <div>
    <template v-if="externalResults && 'nonFieldErrors' in externalResults">
      <DsfrAlert
        v-for="err in externalResults.nonFieldErrors"
        :key="err"
        :description="err"
        type="error"
        :small="true"
        class="mb-2"
      />
    </template>
    <slot />
  </div>
</template>

<script setup>
defineProps({ externalResults: Object })
</script>
