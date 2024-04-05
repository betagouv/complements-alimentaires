<!-- TODO: isoler ce composant car la logique est déliée du reste - voir nuxt mason -->

<!-- <template>
  <div></div>
</template>

<script setup>
// Initial request for gettings countries (TODO: isolate in a component?)

import { onMounted } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"

const {
  data: countryChoices,
  response: countryResponse,
  execute: executeGetCountries,
} = useFetch("/api/v1/countries/", { immediate: false }).json()

onMounted(async () => {
  await executeGetCountries()
  await handleError(countryResponse)
})
</script> -->
