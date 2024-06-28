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
    <DsfrModal size="xl" :opened="modalOpened" @close="modalOpened = false" class="text-left">
      <h2>Version de la déclaration au {{ date }}</h2>
      <DeclarationSummary :readonly="true" v-model="snapshot.jsonDeclaration" />
    </DsfrModal>
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
      <div
        :class="`${rightSide ? 'justify-end' : 'justify-start'} fr-text--sm !mb-0 !text-slate-500 flex gap-4 items-center pb-1`"
      >
        <div>
          {{ date }}
        </div>
        <div>
          <DsfrButton tertiary label="Voir" size="sm" @click="modalOpened = true" />
        </div>
      </div>
      <div>
        {{ snapshot.user.firstName }} {{ snapshot.user.lastName }} a changé le status à «
        <span class="font-bold">{{ statusProps[snapshot.status].label }}</span>
        »
        <span v-if="!snapshot.comment && !isInValidationState">sans laisser de message</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import { statusProps } from "@/utils/mappings"
import { isoToPrettyDate, isoToPrettyTime } from "@/utils/date"
import DeclarationSummary from "@/components/DeclarationSummary"

const props = defineProps({ snapshot: Object, rightSide: Boolean })

const initials = computed(() => `${props.snapshot.user.firstName?.[0]}${props.snapshot.user.lastName?.[0]}`)
const date = computed(
  () => `${isoToPrettyDate(props.snapshot.creationDate)} à ${isoToPrettyTime(props.snapshot.creationDate)}`
)
const modalOpened = ref(false)
const isInValidationState = computed(() => props.snapshot.status === "AWAITING_VISA")
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
