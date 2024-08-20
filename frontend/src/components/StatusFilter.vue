<template>
  <div>
    <DsfrModal :opened="opened" @close="opened = false">
      <DsfrCheckboxSet v-model="statuses" :options="options" />
    </DsfrModal>
    <p class="!mb-2">
      Types de déclaration affichés :

      <span v-if="statuses.length">
        <DsfrTag
          class="mr-2 mt-1"
          v-for="status in statuses"
          :key="`status-${status}`"
          :label="statusProps[status].label"
          small
        />
      </span>
      <span v-else>
        <DsfrTag class="ml-2 mt-1" label="Toutes les déclarations" small />
      </span>
    </p>
    <p>
      <DsfrButton @click="opened = true" tertiary size="small" label="Changer" />
    </p>
  </div>
</template>

<script setup>
import { watch, ref, onMounted } from "vue"
import { statusProps } from "@/utils/mappings"
const statusString = defineModel()
const props = defineProps({ exclude: { type: Array, default: Array }, groupInstruction: { type: Boolean } })
const statuses = ref([])
const opened = ref(false)

onMounted(() => (statuses.value = statusString.value ? statusString.value.split(",") : []))
watch(statuses, () => (statusString.value = statuses.value.join(",")))

const baseFilterOptions = [
  { value: "DRAFT", text: "Brouillon" },
  { value: "OBJECTION", text: "Objection" },
  { value: "OBSERVATION", text: "Observation" },
  { value: "ABANDONED", text: "Abandon" },
  { value: "AUTHORIZED", text: "Déclaration finalisée" },
  { value: "REJECTED", text: "Refus" },
  { value: "WITHDRAWN", text: "Retiré du marché" },
]
const statusFilterOptions = props.groupInstruction
  ? baseFilterOptions
      .slice(0, 1)
      .concat([{ value: "INSTRUCTION", text: "Instruction" }])
      .concat(baseFilterOptions.slice(1))
  : baseFilterOptions
      .slice(0, 1)
      .concat([
        { value: "AWAITING_INSTRUCTION", text: "En attente d'instruction" },
        { value: "ONGOING_INSTRUCTION", text: "En cours d'instruction" },
        { value: "AWAITING_VISA", text: "En attente de visa" },
        { value: "ONGOING_VISA", text: "Visa en cours" },
      ])
      .concat(baseFilterOptions.slice(1))

const options = statusFilterOptions
  .filter((x) => props.exclude.indexOf(x.value) === -1)
  .map((x) => ({ label: x.text, name: x.value }))
</script>
