<template>
  <div>
    <DsfrModal :opened="opened" @close="opened = false" :title="modalTitle">
      <DsfrCheckboxSet v-model="selectedOptions" :options="options" :legend="legend" />
    </DsfrModal>
    <p class="mb-2!">
      {{ filterTitle }} :

      <span v-if="selectedOptions.length">
        <ul class="list-none pl-0 my-0 inline" role="list">
          <li v-for="option in selectedOptions" :key="`filter-opt-${option}`" class="inline">
            <DsfrTag class="mr-2 mt-1" :label="findLabel(option)" small />
          </li>
        </ul>
      </span>
      <span v-else-if="noFilterText">
        <DsfrTag class="ml-2 mt-1" :label="noFilterText" small />
      </span>
    </p>
    <p class="mb-0">
      <DsfrButton @click="opened = true" tertiary size="small">
        Changer
        <span class="sr-only">{{ filterTitle }}</span>
      </DsfrButton>
    </p>
  </div>
</template>

<script setup>
import { watch, ref, onMounted } from "vue"
const emit = defineEmits(["updateFilter"])

const props = defineProps({
  options: { type: Array },
  selectedString: { type: String, required: false },
  filterTitle: { type: String },
  modalTitle: { type: String },
  legend: { type: String },
  noFilterText: { type: String, required: false },
})
const selectedOptions = ref([])
const opened = ref(false)

const updateSelected = () => (selectedOptions.value = props.selectedString ? props.selectedString.split(",") : [])
onMounted(updateSelected)
watch(() => props.selectedString, updateSelected)

watch(selectedOptions, () => emit("updateFilter", selectedOptions.value.join(",")))

const findLabel = (value) => {
  const option = props.options.find((o) => o.value === value)
  return option?.tagLabel || option?.label
}
</script>
