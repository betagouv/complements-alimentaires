<template>
  <div class="grid grid-cols-12 gap-3">
    <FilePreview
      class="col-span-12 sm:col-span-6 md:col-span-4"
      :file="file"
      v-for="file in files"
      :key="file.file"
      @remove="(e) => $emit('remove', e)"
      :hideTypeSelection="hideTypeSelection"
    />
  </div>
</template>

<script setup>
import FilePreview from "@/components/FilePreview"

defineProps({ files: Array, hideTypeSelection: Boolean })
</script>
