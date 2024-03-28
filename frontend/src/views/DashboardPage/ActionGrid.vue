<template>
  <div>
    <h2 class="fr-h5">
      <v-icon class="mr-1 mb-[3px]" :name="icon" v-if="icon" />
      {{ title }}
    </h2>
    <div class="grid grid-cols-12 gap-4">
      <ActionCard
        v-for="(action, index) in props.actions"
        :key="`${action.title}-${index}`"
        :action="props.actions[index]"
        :link="action.link"
        class="col-span-12 sm:col-span-6 md:col-span-4"
      />
    </div>
  </div>
</template>

<script setup>
import ActionCard from "./ActionCard"
const props = defineProps({
  actions: { type: Array, default: () => [] },
  title: { type: String },
  icon: { type: String },
})
</script>
