<template>
  <div class="flex gap-4">
    <div class="rounded-full w-12 h-12 bg-blue-france-925 flex items-center justify-center">
      {{ initials }}
    </div>
    <div class="max-w-xl">
      <div v-if="snapshot.comment" class="italic mb-2 rounded-xl bg-slate-100 p-4 rounded-tl-none">
        {{ snapshot.comment }}
      </div>
      <div>
        {{ isoToPrettyDate(snapshot.creationDate) }} à
        {{ isoToPrettyTime(snapshot.creationDate) }}
      </div>
      <div>
        {{ snapshot.user.firstName }} {{ snapshot.user.lastName }} a changé le statut à «
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
const props = defineProps({ snapshot: Object })

const initials = computed(() => `${props.snapshot.user.firstName?.[0]}${props.snapshot.user.lastName?.[0]}`)
</script>
