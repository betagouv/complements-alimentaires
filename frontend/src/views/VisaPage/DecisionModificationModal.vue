<template>
  <div>
    <div class="text-right">
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
      <div class="grid grid-cols-2 gap-4">
        <div class="col-span-2 sm:col-span-1">
          <DsfrInputGroup>
            <DsfrSelect
              label="Nouvelle décision"
              v-model="overridenDecision.proposal"
              :options="proposalOptions"
              class="max-w-96"
            />
          </DsfrInputGroup>
        </div>
        <div class="col-span-2 sm:col-span-1">
          <DsfrInputGroup>
            <DsfrInput
              v-model="overridenDecision.delayDays"
              label="Délai de réponse (jours)"
              label-visible
              class="max-w-96"
            />
          </DsfrInputGroup>
        </div>
      </div>
      <DsfrInputGroup>
        <DsfrInput
          is-textarea
          label="Message au déclarant·e"
          v-model="overridenDecision.producerMessage"
          label-visible
        />
      </DsfrInputGroup>
      <div v-if="showReasons" class="border p-4">
        <DsfrInputGroup>
          <div class="mb-8" v-for="reason in blockingReasons" :key="reason.title">
            <p class="font-bold">{{ reason.title }}</p>
            <DsfrCheckboxSet
              v-model="overridenDecision.reasons"
              :options="reason.items.map((x) => ({ label: x, value: x }))"
            />
          </div>
        </DsfrInputGroup>
      </div>
    </DsfrModal>
  </div>
</template>

<script setup>
import { ref, computed, onUpdated } from "vue"
import { blockingReasons } from "@/utils/mappings"
const emit = defineEmits(["override"])
const props = defineProps({ originalOverridenDecision: { type: Object, default: () => {} } })

const overridenDecision = ref(props.originalOverridenDecision || {})

const opened = ref(false)

const actions = [
  {
    label: "Modifier la décision",
    onClick: () => emit("override", overridenDecision.value),
    icon: { name: "ri-edit-fill" },
  },
  {
    label: "Annuler",
    onClick: () => close(),
    secondary: true,
  },
]

const close = () => (opened.value = false)
const open = () => (opened.value = true)

const proposalOptions = [
  { text: "Autorisation", value: "autorisation" },
  { text: "Observation", value: "observation" },
  { text: "Objection", value: "objection" },
  { text: "Refus", value: "rejection" },
]

const showReasons = computed(
  () => overridenDecision.value.proposal && overridenDecision.value.proposal !== "autorisation"
)

onUpdated(() => (overridenDecision.value = props.originalOverridenDecision || {}))
</script>
