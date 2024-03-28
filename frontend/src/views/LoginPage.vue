<template>
  <SingleItemWrapper>
    <h1>Se connecter</h1>
    <FormWrapper :externalResults="$externalResults">
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'username')">
        <DsfrInput v-model="state.username" label="Identifiant" labelVisible autofocus />
      </DsfrInputGroup>
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'password')">
        <DsfrInput :type="showPassword ? 'text' : 'password'" v-model="state.password" labelVisible>
          <template #label>
            <div class="flex items-center justify-between">
              <div>Mot de passe</div>
              <DsfrButton
                @click="showPassword = !showPassword"
                :label="showPassword ? 'Cacher' : 'Afficher'"
                :icon="showPassword ? 'ri-eye-off-line' : 'ri-eye-line'"
                size="sm"
                tertiary
                noOutline
              />
            </div>
          </template>
        </DsfrInput>
        <div class="mt-2">
          <a class="fr-link" href="#">Mot de passe oublié ?</a>
        </div>
      </DsfrInputGroup>
      <DsfrButton class="!block !w-full" :disabled="isFetching" label="Se connecter" @click="submit" />
      <hr class="mt-8" />
      <h4>Vous n'avez pas de compte ?</h4>
      <DsfrButton class="!block !w-full" secondary label="S'enregistrer" @click="router.push('/inscription')" />
    </FormWrapper>
  </SingleItemWrapper>
</template>

<script setup>
import { ref } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import { errorRequiredField, firstErrorMsg } from "@/utils/forms"
import useToaster from "@/composables/use-toaster"
import { handleError } from "@/utils/error-handling"
import { useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import FormWrapper from "@/components/FormWrapper"
import SingleItemWrapper from "@/components/SingleItemWrapper"

const router = useRouter()
const rootStore = useRootStore()

const showPassword = ref(false)

// Form state & rules
const state = ref({
  username: "",
  password: "",
})

const rules = {
  username: errorRequiredField,
  password: errorRequiredField,
}

const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

// Request definition
const { data, response, execute, isFetching } = useFetch(
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
  $externalResults.value = await handleError(response)

  if (response.value.ok) {
    {
      await rootStore.fetchInitialData()
      window.CSRF_TOKEN = data.value.csrfToken
      useToaster().addMessage({
        type: "success",
        title: "Vous êtes connecté",
        description: "Vous êtes connecté à la plateforme Compl'Alim.",
      })
      router.push({ name: "DashboardPage" })
    }
  }
}
</script>
