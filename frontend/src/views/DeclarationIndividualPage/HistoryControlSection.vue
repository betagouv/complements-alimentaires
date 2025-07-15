<template>
  <HistorySection :snapshots="snapshots" :hideInstructionDetails="true" />
</template>

<script setup>
import HistorySection from "@/components/NewBepiasViews/HistorySection"
defineProps({ snapshots: Array })
</script>
