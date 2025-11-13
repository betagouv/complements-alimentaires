<template>
  <div>
    <div class="text-right">
      <DsfrButton
        v-if="showUndoButton"
        label="Annuler la modification"
        size="sm"
        secondary
        icon="ri-close-fill"
        @click="undo"
        class="mr-2"
      />
      <DsfrButton label="Modifier la décision" size="sm" secondary icon="ri-edit-fill" @click="open" />
    </div>

    <DsfrModal
      :actions="actions"
      ref="modal"
      @close="close"
      :opened="opened"
      title="Modifier la décision de l'instruction"
      size="xl"
    >
      <div class="grid grid-cols-2 gap-4 mb-2">
        <div class="col-span-2 sm:col-span-1">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'proposal')">
            <DsfrSelect
              label="Nouvelle décision"
              v-model="overriddenDecision.proposal"
              :options="proposalOptions"
              class="max-w-96"
            />
          </DsfrInputGroup>
        </div>
        <div class="col-span-2 sm:col-span-1" v-if="showDelayDays">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'delayDays')">
            <DsfrInput
              v-model="overriddenDecision.delayDays"
              label="Délai de réponse (jours)"
              label-visible
              class="max-w-96"
            />
          </DsfrInputGroup>
        </div>
      </div>
      <div v-if="showAdditionalFields" class="border p-4">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'comment')">
          <DsfrInput is-textarea label="Message au déclarant·e" v-model="overriddenDecision.comment" label-visible />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'reasons')">
          <div class="mb-8" v-for="reason in blockingReasons" :key="reason.title">
            <DsfrCheckboxSet
              v-model="overriddenDecision.reasons"
              :options="reason.items.map((x) => ({ label: x, value: x }))"
              :legend="reason.title"
            />
          </div>
        </DsfrInputGroup>
      </div>
    </DsfrModal>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { blockingReasons } from "@/utils/mappings"
import { errorRequiredField, errorInteger, firstErrorMsg } from "@/utils/forms"
import { helpers, required } from "@vuelidate/validators"
import { useVuelidate } from "@vuelidate/core"

const modelValue = defineModel()
const overriddenDecision = ref()

const copyModelValueToRef = () =>
  (overriddenDecision.value = modelValue.value ? JSON.parse(JSON.stringify(modelValue.value)) : { reasons: [] })

copyModelValueToRef()

const rules = computed(() => {
  if (!overriddenDecision.value?.proposal) return { proposal: errorRequiredField }
  if (overriddenDecision.value?.proposal === "AUTHORIZED") return {}
  return {
    comment: errorRequiredField,
    reasons: { required: helpers.withMessage("Au moins une raison doit être selectionnée", required) },
    proposal: errorRequiredField,
    delayDays:
      overriddenDecision.value?.proposal !== "REJECTED" ? Object.assign({}, errorRequiredField, errorInteger) : {},
  }
})

const $externalResults = ref({})
const v$ = useVuelidate(rules, overriddenDecision, { $externalResults })

const opened = ref(false)

const actions = [
  {
    label: "Modifier la décision",
    onClick: () => {
      v$.value.$reset()
      v$.value.$validate()
      if (v$.value.$error) return
      modelValue.value = overriddenDecision.value
      close()
    },
    icon: { name: "ri-edit-fill" },
  },
  {
    label: "Annuler",
    onClick: () => close(),
    secondary: true,
  },
]

const close = () => {
  opened.value = false
  copyModelValueToRef()
}
const open = () => {
  v$.value.$reset()
  opened.value = true
}
const undo = () => (modelValue.value = undefined)

const showUndoButton = computed(() => !!modelValue.value?.proposal)

const proposalOptions = [
  { text: "Autorisation", value: "AUTHORIZED" },
  { text: "Observation", value: "OBSERVATION" },
  { text: "Objection", value: "OBJECTION" },
  { text: "Refus", value: "REJECTED" },
]

const showAdditionalFields = computed(
  () => overriddenDecision.value.proposal && overriddenDecision.value.proposal !== "AUTHORIZED"
)

const showDelayDays = computed(
  () => overriddenDecision.value.proposal === "OBSERVATION" || overriddenDecision.value.proposal === "OBJECTION"
)

watch(modelValue, () => copyModelValueToRef())
</script>

<style scoped>
@reference "../../styles/index.css";
div :deep(.fr-fieldset__legend) {
  @apply font-bold!;
}
</style>
