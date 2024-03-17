<template>
  <div class="mx-auto max-w-72 p-4 rounded-lg my-24">
    <h1 class="text-center">Connexion</h1>
    <DsfrInputGroup :error-message="firstErrorMsg(v$, 'username')">
      <DsfrInput v-model="state.username" label="Nom d'utilisateur" :labelVisible="true" />
    </DsfrInputGroup>
    <DsfrInputGroup :error-message="firstErrorMsg(v$, 'password')">
      <DsfrInput type="password" v-model="state.password" label="Mot de passe" :labelVisible="true" />
    </DsfrInputGroup>
    <DsfrButton class="!block !w-full" :disabled="isFetching" label="Valider" @click="submit" />
    <div class="text-center">
      <DsfrButton class="mt-5" label="Mot de passe oublié ?" tertiary noOutline size="sm" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, helpers } from "@vuelidate/validators"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import { firstErrorMsg } from "@/utils/forms"
import useToaster from "@/composables/use-toaster"
import { useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"

const router = useRouter()
const rootStore = useRootStore()

// Form state & rules
const state = ref({
  username: "",
  password: "",
})

const rules = {
  username: { required: helpers.withMessage("Ce champ doit être rempli", required) },
  password: { required: helpers.withMessage("Ce champ doit être rempli", required) },
}

const v$ = useVuelidate(rules, state)

// Request definition
const { data, error, execute, isFetching } = useFetch(
  "/api/v1/login/",
  {
    headers: headers(),
  },
  { immediate: false }
)
  .post(state)
  .json()

// Form validation
const submit = async () => {
  v$.value.$validate()
  if (v$.value.$error) {
    return // prevent API call if there is a front-end error
  }
  await execute()

  const { addMessage, addUnknownErrorMessage } = useToaster()
  if (error.value) {
    addUnknownErrorMessage() // TODO: we need to get actual backend errors here!
  } else {
    await rootStore.fetchInitialData()
    window.CSRF_TOKEN = data.value.csrfToken
    addMessage({
      type: "success",
      title: "Vous êtes connecté",
      description: "Vous êtes connecté à la plateforme Compl'Alim.",
    })
    router.push({ name: "DashboardPage" })
  }
}
</script>
