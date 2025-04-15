<template>
  <DsfrSelect
    defaultUnselectedText="Choisissez un pays"
    :options="countries"
    label="Pays"
    :required="required"
    labelVisible
  />
</template>

<script setup>
import { onMounted, computed } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"

const { data, response, execute } = useFetch("/api/v1/countries/", { immediate: false }).json()
const props = defineProps({
  exclude: { default: Array() },
  required: { default: false },
  includeAllOption: { default: false },
})
const countries = computed(() => {
  const filteredCountries = data.value?.filter((x) => props.exclude.indexOf(x.value) === -1) || []
  if (props.includeAllOption) {
    filteredCountries.unshift({ disabled: true, text: "---------" })
    filteredCountries.unshift({ value: "", text: "Tout afficher" })
  }
  return filteredCountries
})

onMounted(async () => {
  await execute()
  await handleError(response)
})
</script>
