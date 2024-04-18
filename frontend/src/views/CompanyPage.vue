<template>
  <div v-if="company" class="fr-container my-8 flex flex-col">
    <h1>{{ company.socialName }}</h1>
  </div>
</template>

<script setup>
import { onMounted } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { useRoute } from "vue-router"
import { headers } from "@/utils/data-fetching"

const route = useRoute()

const {
  data: company,
  response,
  execute,
} = useFetch(
  `/api/v1/companies/${route.params.id}`,
  {
    headers: headers(),
  },
  { immediate: false }
).json()

onMounted(async () => {
  await execute()
  await handleError(response)
})
</script>
