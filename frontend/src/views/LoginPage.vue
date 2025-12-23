<template>
  <SingleItemWrapper>
    <h1>Se connecter</h1>
    <FormWrapper :externalResults="$externalResults">
      <SendNewSignupVerificationEmail v-if="showSendNewConfirmationMail" :userId="userIdForNewConfirmationMail" />
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'username')">
        <DsfrInput v-model="state.username" label="Identifiant ou adresse email" labelVisible @keyup.enter="submit" />
      </DsfrInputGroup>
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'password')">
        <DsfrInput
          :type="showPassword ? 'text' : 'password'"
          v-model="state.password"
          labelVisible
          @keyup.enter="submit"
        >
          <template #label>
            <div class="flex items-center justify-between">
              <div>Mot de passe</div>
              <PasswordDisplayToggle :showPassword="showPassword" @update:showPassword="showPassword = $event" />
            </div>
          </template>
        </DsfrInput>
        <div class="mt-2">
          <a class="fr-link" href="/reinitialisation-mot-de-passe">Mot de passe oublié ?</a>
        </div>
      </DsfrInputGroup>
      <DsfrButton class="block! w-full!" :disabled="isFetching" label="Se connecter" @click="submit" />
      <hr class="mt-8" />
      <h4>Vous n'avez pas de compte ?</h4>
      <DsfrButton class="block! w-full!" secondary label="S'enregistrer" @click="router.push({ name: 'SignupPage' })" />
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
import { useRouter, useRoute } from "vue-router"
import { useRootStore } from "@/stores/root"
import FormWrapper from "@/components/FormWrapper"
import SingleItemWrapper from "@/components/SingleItemWrapper"
import SendNewSignupVerificationEmail from "@/components/SendNewSignupVerificationEmail"
import PasswordDisplayToggle from "@/components/PasswordDisplayToggle"

const router = useRouter()
const route = useRoute()
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

const showSendNewConfirmationMail = ref(false)
const userIdForNewConfirmationMail = ref()

// Form validation
const submit = async () => {
  v$.value.$validate()
  if (v$.value.$error) {
    return // prevent API call if there is a front-end error
  }
  await execute()
  $externalResults.value = await handleError(response)

  // Give the ability to ask for a new e-email, only if the user is not verified yet.
  // ⛔️ TODO: change this dirty hack: we use error message until having appropriate error codes in responses
  if ($externalResults.value?.nonFieldErrors?.[0]?.includes("vérifié")) {
    showSendNewConfirmationMail.value = true
    userIdForNewConfirmationMail.value = `${$externalResults.value.extra.userId}`
  }

  if (response.value.ok) {
    {
      await rootStore.fetchInitialData()
      window.CSRF_TOKEN = data.value.csrfToken
      useToaster().addMessage({
        type: "success",
        title: "Vous êtes connecté",
        description: "Vous êtes connecté à la plateforme Compl'Alim.",
      })
      router.push(route.query.next || { name: "DashboardPage" })
    }
  }
}
</script>
