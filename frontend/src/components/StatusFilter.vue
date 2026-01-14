<template>
  <div>
    <MultiselectFilter
      :options="options"
      :selectedString="statusString"
      filterTitle="Types de déclaration affichés :"
      modalTitle="Changer les déclarations affichées"
      legend="Type de déclaration"
      noFilterText="Toutes les déclarations"
      @updateFilter="emitUpdate"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { statusProps } from "@/utils/mappings"
import MultiselectFilter from "./MultiselectFilter"
const emit = defineEmits(["updateFilter"])
const props = defineProps({
  exclude: { type: Array, default: Array },
  groupInstruction: { type: Boolean },
  statusString: { type: String },
})
const statuses = ref([])

onMounted(() => (statuses.value = props.statusString ? props.statusString.split(",") : []))
const emitUpdate = (v) => emit("updateFilter", v)

const baseFilterOptions = [
  { value: "DRAFT", label: "Brouillon" },
  { value: "OBJECTION", label: "Objection" },
  { value: "OBSERVATION", label: "Observation" },
  { value: "ABANDONED", label: "Abandon" },
  { value: "AUTHORIZED", label: "Déclaration finalisée" },
  { value: "REJECTED", label: "Refus" },
  { value: "WITHDRAWN", label: "Retiré du marché" },
  { value: "AUTHORIZATION_REVOKED", label: "Retiré du marché par l'administration" },
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
  .map((x) => ({ label: x.label, value: x.value, tagLabel: statusProps[x.value].label }))
</script>
