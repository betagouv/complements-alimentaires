<template>
  <div>
    <div class="grid grid-cols-2 gap-4 mb-2">
      <div class="col-span-2 sm:col-span-1">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'proposal')">
          <DsfrSelect
            label="Nouvelle décision"
            v-model="modelValue.proposal"
            :options="proposalOptions"
            class="max-w-96"
          />
        </DsfrInputGroup>
      </div>
      <div class="col-span-2 sm:col-span-1" v-if="showDelayDays">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'delayDays')">
          <DsfrInput v-model="modelValue.delayDays" label="Délai de réponse (jours)" label-visible class="max-w-96" />
        </DsfrInputGroup>
      </div>
    </div>
    <div v-if="showAdditionalFields" class="border p-4">
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'comment')">
        <DsfrInput is-textarea label="Message au déclarant·e" v-model="modelValue.comment" label-visible />
      </DsfrInputGroup>
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'reasons')">
        <div class="mb-8" v-for="reason in blockingReasons" :key="reason.title">
          <DsfrCheckboxSet
            v-model="modelValue.reasons"
            :options="reason.items.map((x) => ({ label: x, value: x }))"
            :legend="reason.title"
          />
        </div>
      </DsfrInputGroup>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { blockingReasons } from "@/utils/mappings"
import { errorRequiredField, errorInteger, firstErrorMsg } from "@/utils/forms"
import { helpers, required } from "@vuelidate/validators"
import { useVuelidate } from "@vuelidate/core"

const modelValue = defineModel()

const rules = computed(() => {
  if (!modelValue.value?.proposal) return { proposal: errorRequiredField }
  if (modelValue.value?.proposal === "AUTHORIZED") return {}
  return {
    comment: errorRequiredField,
    reasons: { required: helpers.withMessage("Au moins une raison doit être selectionnée", required) },
    proposal: errorRequiredField,
    delayDays: modelValue.value?.proposal !== "REJECTED" ? Object.assign({}, errorRequiredField, errorInteger) : {},
  }
})

const $externalResults = ref({})
const v$ = useVuelidate(rules, modelValue, { $externalResults })

const proposalOptions = [
  { text: "Autorisation", value: "AUTHORIZED" },
  { text: "Observation", value: "OBSERVATION" },
  { text: "Objection", value: "OBJECTION" },
  { text: "Refus", value: "REJECTED" },
]

const showAdditionalFields = computed(() => modelValue.value.proposal && modelValue.value.proposal !== "AUTHORIZED")

const showDelayDays = computed(
  () => modelValue.value.proposal === "OBSERVATION" || modelValue.value.proposal === "OBJECTION"
)

const validate = () => {
  v$.value.$reset()
  v$.value.$validate()
  return v$.value.$error
}

defineExpose({ validate })
</script>

<style scoped>
@reference "../../styles/index.css";
div :deep(.fr-fieldset__legend) {
  @apply font-bold!;
}
</style>
