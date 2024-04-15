<template>
  <DsfrSelect defaultUnselectedText="Choisissez un pays" :options="data" label="Pays" required labelVisible />
</template>

<script setup>
import { onMounted } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"

const { data, response, execute } = useFetch("/api/v1/countries/", { immediate: false }).json()

onMounted(async () => {
  await execute()
  await handleError(response)
})
</script>
