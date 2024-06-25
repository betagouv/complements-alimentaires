<template>
  <div
    :class="{
      flex: true,
      'gap-4': true,
      'flex-row-reverse': rightSide,
      'text-right': rightSide,
      'right-side': rightSide,
    }"
  >
    <div class="initials rounded-full min-w-12 w-12 h-12 flex items-center justify-center">
      {{ initials }}
    </div>
    <div class="max-w-xl">
      <div :class="`flex ${rightSide ? 'justify-end' : 'justify-start'}`">
        <div
          v-if="snapshot.comment"
          :class="`comment italic mb-2 rounded-xl p-4 ${rightSide ? 'rounded-tr-none' : 'rounded-tl-none'}`"
        >
          {{ snapshot.comment }}
        </div>
      </div>
      <div class="fr-text--sm !mb-0 !text-slate-500">
        {{ isoToPrettyDate(snapshot.creationDate) }} à
        {{ isoToPrettyTime(snapshot.creationDate) }}
      </div>
      <div>
        {{ snapshot.user.firstName }} {{ snapshot.user.lastName }} a changé le status à «
        <span class="font-bold">{{ statusProps[snapshot.status].label }}</span>
        »
        <span v-if="!snapshot.comment">sans laisser de message</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { statusProps } from "@/utils/mappings"
import { isoToPrettyDate, isoToPrettyTime } from "@/utils/date"
const props = defineProps({ snapshot: Object, rightSide: Boolean })

const initials = computed(() => `${props.snapshot.user.firstName?.[0]}${props.snapshot.user.lastName?.[0]}`)
</script>

<style scoped>
.initials,
.comment {
  @apply bg-blue-france-950;
}
.right-side .initials,
.right-side .comment {
  @apply bg-slate-100;
}
</style>
