<template>
  <div>
    <SectionTitle :title="title" :icon="icon" />
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
import SectionTitle from "@/components/SectionTitle"
import ActionCard from "./ActionCard"

const props = defineProps({
  actions: { type: Array, default: () => [] },
  title: { type: String },
  icon: { type: String },
})
</script>
