<template>
  <h2>
    <v-icon :name="icon" scale="1.4" class="block mt-[6px] mr-2 float-left" />
    {{ text }}
  </h2>
</template>

<script setup>
defineProps(["icon", "text"])
</script>
