<template>
  <div class="grid grid-cols-12 gap-4">
    <ActionCard
      v-for="(action, index) in props.actions"
      :key="`${action.title}-${index}`"
      :action="props.actions[index]"
      class="col-span-12 sm:col-span-6 md:col-span-4"
    />
  </div>
</template>

<script setup>
import ActionCard from "./ActionCard"
const props = defineProps({ actions: { type: Array, default: () => [] } })
</script>
