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
      <v-icon v-if="hideInstructionDetails && isAdministrativeAction" name="ri-user-fill" aria-hidden />
      <span v-else>{{ initials }}</span>
    </div>
    <div class="max-w-xl">
      <div :class="`flex ${rightSide ? 'justify-end' : 'justify-start'}`">
        <div
          v-if="showComment"
          :class="`comment italic mb-2 rounded-xl p-4 ${rightSide ? 'rounded-tr-none' : 'rounded-tl-none'}`"
        >
          {{ snapshot.comment }}
        </div>
      </div>
      <div
        :class="`${rightSide ? 'justify-end' : 'justify-start'} fr-text--sm mb-0! text-slate-500! flex gap-4 items-center pb-1`"
      >
        <div>
          {{ date }}
        </div>
        <div>
          <DsfrButton tertiary label="Voir" size="sm" @click="modalOpened = true" />
        </div>
      </div>
      <div v-if="actionText">
        {{ actionText }}
      </div>
      <div v-else>
        {{ fullName }} a changé le statut à « {{ statusProps[snapshot.status].label }} »
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

const props = defineProps({ snapshot: Object, rightSide: Boolean, hideInstructionDetails: Boolean })

const isAdministrativeAction = computed(() => {
  const instructionActions = [
    "TAKE_FOR_INSTRUCTION",
    "OBSERVE_NO_VISA",
    "AUTHORIZE_NO_VISA",
    "REQUEST_VISA",
    "TAKE_FOR_VISA",
    "APPROVE_VISA",
    "REFUSE_VISA",
  ]
  return instructionActions.indexOf(props.snapshot.action) > -1
})

const showComment = computed(() => props.snapshot?.comment && props.snapshot?.action !== "REFUSE_VISA")

const initials = computed(() => {
  if (!props.snapshot.user) return "?"
  return `${props.snapshot.user.firstName?.[0]}${props.snapshot.user.lastName?.[0]}`
})
const date = computed(
  () => `${isoToPrettyDate(props.snapshot.creationDate)} à ${isoToPrettyTime(props.snapshot.creationDate)}`
)
const modalOpened = ref(false)
const isInValidationState = computed(() => props.snapshot.status === "AWAITING_VISA")
const fullName = computed(() => {
  if (props.hideInstructionDetails && isAdministrativeAction.value) return "L'administration"
  if (!props.snapshot.user) return "Une personne"
  return `${props.snapshot.user.firstName} ${props.snapshot.user.lastName}`
})
const actionText = computed(() => {
  const mapping = {
    SUBMIT: "a soumis la déclaration pour instruction",
    OBSERVE_NO_VISA: "a emis des observations",
    AUTHORIZE_NO_VISA: "a autorisé la déclaration",
    RESPOND_TO_OBSERVATION: "a répondu aux observations",
    RESPOND_TO_OBJECTION: "a répondu aux objections",
    REQUEST_VISA: `a demandé un visa pour passer à l'état « ${statusProps[props.snapshot.postValidationStatus]?.label} »`,
    APPROVE_VISA: `a mis la déclaration en état « ${statusProps[props.snapshot.postValidationStatus]?.label} »`,
    REFUSE_VISA: `a refusé le visa pour passer à l'état « ${statusProps[props.snapshot.postValidationStatus]?.label} »`,
    WITHDRAW: getWithdrawalText(props.snapshot),
  }
  return mapping[props.snapshot.action] ? `${fullName.value} ${mapping[props.snapshot.action]}.` : null
})

const getWithdrawalText = (snapshot) => {
  const baseText = "a retiré le produit du marché"
  if (!snapshot.effectiveWithdrawalDate) return baseText
  return `${baseText} (date effective : ${isoToPrettyDate(snapshot.effectiveWithdrawalDate)})`
}
</script>

<style scoped>
@reference "../../styles/index.css";

.initials,
.comment {
  @apply bg-blue-france-950;
  white-space: pre-line;
}
.right-side .initials,
.right-side .comment {
  @apply bg-slate-100;
}
</style>
