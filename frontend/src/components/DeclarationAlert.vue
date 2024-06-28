<template>
  <DsfrAlert
    :type="status === 'AUTHORIZED' ? 'success' : 'info'"
    :title="`Cette déclaration est en status « ${statusProps[status].label} »`"
  />
</template>

<script setup>
import { statusProps } from "@/utils/mappings"
defineProps({ status: String })
</script>
