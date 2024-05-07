<template>
  <div>
    <SectionTitle :title="title" :icon="icon" />
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <ActionCard
        v-for="(action, index) in props.actions"
        :key="`${action.title}-${index}`"
        :action="props.actions[index]"
        :link="action.link"
      />
    </div>
  </div>
</template>

<script setup>
import SectionTitle from "@/components/SectionTitle"
import ActionCard from "./ActionCard"

const props = defineProps({
  actions: { type: Array, default: () => [] },
  title: { type: String },
  icon: { type: String },
})
</script>
