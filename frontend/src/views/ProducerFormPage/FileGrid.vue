<template>
  <div class="grid grid-cols-12 gap-3">
    <FilePreview
      class="col-span-12 sm:col-span-6 md:col-span-4"
      :file="file"
      v-for="file in props.files"
      :key="file.file"
      @remove="(e) => $emit('remove', e)"
      :hideTypeSelection="props.hideTypeSelection"
    />
  </div>
</template>

<script setup>
import FilePreview from "@/components/FilePreview"

const props = defineProps({ files: Array, hideTypeSelection: Boolean })
</script>
