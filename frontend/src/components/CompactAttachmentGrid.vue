<template>
  <div class="grid grid-cols-12 gap-3 mb-8">
    <p
      class="col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-3 mb-0"
      v-for="(file, index) in attachments"
      :key="`file-download-${index}`"
    >
      <a :title="`${file.name} - nouvelle fenêtre`" :href="file.file" target="_blank" class="fr-link">
        <span>{{ truncateMiddle(file.name, 20) }}</span>
        <span class="fr-sr-only">&nbsp;- nouvelle fenêtre</span>
      </a>
      <span class="fr-link__detail fr-text--xs block mb-0">{{ file.typeDisplay }} - {{ file.size }}</span>
    </p>
  </div>
</template>

<script setup>
import { truncateMiddle } from "@/utils/string"
defineProps({ attachments: Array })
</script>
