<template>
  <div>
    <DsfrModal :opened="opened" @close="opened = false">
      <DsfrCheckboxSet v-model="statuses" :options="options" />
    </DsfrModal>
    <p class="mb-2!">
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
const emit = defineEmits(["updateFilter"])
const statusString = defineModel()
const props = defineProps({ exclude: { type: Array, default: Array }, groupInstruction: { type: Boolean } })
const statuses = ref([])
const opened = ref(false)

onMounted(() => (statuses.value = statusString.value ? statusString.value.split(",") : []))
watch(statuses, () => emit("updateFilter", statuses.value.join(",")))

const baseFilterOptions = [
  { value: "DRAFT", label: "Brouillon" },
  { value: "OBJECTION", label: "Objection" },
  { value: "OBSERVATION", label: "Observation" },
  { value: "ABANDONED", label: "Abandon" },
  { value: "AUTHORIZED", label: "Déclaration finalisée" },
  { value: "REJECTED", label: "Refus" },
  { value: "WITHDRAWN", label: "Retiré du marché" },
]
const statusFilterOptions = props.groupInstruction
  ? baseFilterOptions
      .slice(0, 1)
      .concat([{ value: "INSTRUCTION", label: "Instruction" }])
      .concat(baseFilterOptions.slice(1))
  : baseFilterOptions
      .slice(0, 1)
      .concat([
        { value: "AWAITING_INSTRUCTION", label: "En attente d'instruction" },
        { value: "ONGOING_INSTRUCTION", label: "En cours d'instruction" },
        { value: "AWAITING_VISA", label: "En attente de visa" },
        { value: "ONGOING_VISA", label: "Visa en cours" },
      ])
      .concat(baseFilterOptions.slice(1))

const options = statusFilterOptions
  .filter((x) => props.exclude.indexOf(x.value) === -1)
  .map((x) => ({ label: x.label, value: x.value }))
</script>
