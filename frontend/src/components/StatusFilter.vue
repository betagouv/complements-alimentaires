<template>
  <div>
    <DsfrModal :opened="opened" @close="opened = false">
      <DsfrCheckboxSet v-model="statuses" :options="options" />
    </DsfrModal>
    <p class="!mb-2">
      Types de déclaration afficheés :

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
const props = defineProps({ exclude: { type: Array, default: Array } })
const statuses = ref([])
const opened = ref(false)

onMounted(() => (statuses.value = statusString.value ? statusString.value.split(",") : []))
watch(statuses, () => {
  statusString.value = statuses.value.join(",")
})
const statusFilterOptions = [
  { value: "DRAFT", text: "Brouillon" },
  { value: "AWAITING_INSTRUCTION", text: "En attente d'instruction" },
  { value: "ONGOING_INSTRUCTION", text: "En cours d'instruction" },
  { value: "AWAITING_VISA", text: "En attente de visa" },
  { value: "ONGOING_VISA", text: "Visa en cours" },
  { value: "OBJECTION", text: "Objection" },
  { value: "OBSERVATION", text: "Observation" },
  { value: "ABANDONED", text: "Abandon" },
  { value: "AUTHORIZED", text: "Autorisée" },
  { value: "REJECTED", text: "Refusée" },
]
const options = statusFilterOptions
  .filter((x) => props.exclude.indexOf(x.value) === -1)
  .map((x) => ({ label: x.text, name: x.value }))
</script>
