<template>
  <div class="flex gap-px">
    <div class="h-3 w-3 rounded-full bg-red-500" v-if="hasRefusedVisa"></div>
    <div class="h-3 w-3 rounded-full bg-orange-400" v-if="hasPendingProResponses"></div>
  </div>
</template>

<script setup>
import { computed } from "vue"
const props = defineProps(["declaration"])

const hasPendingProResponses = computed(() => props.declaration.hasPendingProResponses)
const hasRefusedVisa = computed(() => props.declaration.visaRefused)
</script>
