<template>
  <div class="grid grid-cols-12 gap-3 mb-8">
    <div
      class="col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-3 overflow-auto"
      v-for="(file, index) in attachments"
      :key="`file-download-${index}`"
    >
      <DsfrFileDownload
        :title="`${truncateMiddle(file.name, 20)}`"
        :href="file.file"
        :size="file.size"
        :format="file.typeDisplay"
        :download="null"
        target="_blank"
      />
    </div>
  </div>
</template>

<script setup>
import { truncateMiddle } from "@/utils/string"
defineProps({ attachments: Array })
</script>
