<script setup>
import { useFetch } from "@vueuse/core"
import { onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"
import { useRootStore } from "@/stores/root"

const route = useRoute()
const router = useRouter()
const { addSuccessMessage } = useToaster()
const rootStore = useRootStore()

// Request definition
const { data, response, execute } = useFetch("/api/v1/verify-email/", { headers: headers() }, { immediate: false })
  .post(route.query)
  .json()

onMounted(async () => {
  await execute()
  await handleError(response)
  if (response.value.ok) {
    await rootStore.fetchInitialData()
    window.CSRF_TOKEN = data.value.csrfToken
    addSuccessMessage("Votre compte a bien été validé. Vous êtes connecté à la plate-forme Compl'Alim.")
    router.push({ name: "DashboardPage" })
  }
})
</script>
