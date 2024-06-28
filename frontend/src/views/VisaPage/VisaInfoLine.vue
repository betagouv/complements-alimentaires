<template>
  <div class="sm:flex border-b last:border-0 py-3 gap-4">
    <div class="sm:flex-[0_0_25%] font-bold">
      <v-icon class="mr-2" :name="icon" aria-hidden />
      <span>{{ title }}</span>
    </div>
    <div class="sm:flex-auto">
      {{ text }}
    </div>
  </div>
</template>

<script setup>
defineProps(["icon", "title", "text"])
</script>
