<template>
  <div class="fr-container my-6">
    <div v-if="isFetching" class="flex justify-center">
      <ProgressSpinner />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import ProgressSpinner from "@/components/ProgressSpinner"
import useToaster from "@/composables/use-toaster"
import { useRootStore } from "@/stores/root"

const { addMessage, addUnknownErrorMessage } = useToaster()
const router = useRouter()
const rootStore = useRootStore()

const { error, execute, isFetching } = useFetch("/api/v1/logout/", { immediate: false }).post()

const logout = async () => {
  await execute()
  if (error.value) {
    addUnknownErrorMessage()
  } else {
    await rootStore.resetInitialData()
    router.replace({ name: "LandingPage" })
    addMessage({
      type: "success",
      title: "Vous êtes déconnecté",
      description: "Vous avez été déconnecté de la plateforme.",
    })
  }
}

logout()
</script>
