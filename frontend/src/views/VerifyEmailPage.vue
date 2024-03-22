<script setup>
import { useFetch } from "@vueuse/core"
import { onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"

const route = useRoute()
const router = useRouter()
const { addSuccessMessage } = useToaster()

// Request definition
const { response, execute } = useFetch("/api/v1/verify-email/", { headers: headers() }, { immediate: false })
  .post(route.query)
  .json()

onMounted(async () => {
  await execute()
  await handleError(response)
  if (response.value.ok) {
    addSuccessMessage("Votre compte a bien été validé. Vous pouvez maintenant vous connecter.")
    router.push({ name: "LoginPage" })
  }
})
</script>
