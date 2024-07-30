<template>
  <div class="border p-4 bg-gray-100 text-right">
    <DsfrButton
      secondary
      v-if="selectedTabIndex > 0"
      @click="emit('back')"
      :label="`Revenir à l'onglet « ${titles[selectedTabIndex - 1].title} »`"
    />
    <DsfrButton
      class="ml-4"
      v-if="selectedTabIndex < titles.length - 1"
      @click="emit('forward')"
      :label="`Passer à l'onglet « ${titles[selectedTabIndex + 1].title} »`"
    />
  </div>
</template>

<script setup>
defineProps(["titles", "selectedTabIndex"])
const emit = defineEmits(["back", "forward"])
</script>
