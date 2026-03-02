<template>
  <SingleItemWrapper>
    <h1>Se créer un compte</h1>
    <FormWrapper :externalResults="$externalResults">
      <p class="fr-hint-text">Sauf mention contraire, tous les champs sont obligatoires.</p>
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'lastName')">
        <DsfrInput
          v-model="state.lastName"
          label="Nom"
          labelVisible
          type="text"
          spellcheck="false"
          autocomplete="family-name"
        />
      </DsfrInputGroup>
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'firstName')">
        <DsfrInput
          v-model="state.firstName"
          label="Prénom"
          labelVisible
          type="text"
          spellcheck="false"
          autocomplete="given-name"
        />
      </DsfrInputGroup>
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'email')">
        <DsfrInput
          v-model="state.email"
          label="Adresse e-mail"
          labelVisible
          type="email"
          hint="Elle sera nécessaire pour valider la création de votre compte."
          autocomplete="email"
          spellcheck="false"
        />
      </DsfrInputGroup>
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'username')">
        <DsfrInput
          v-model="state.username"
          label="Identifiant"
          labelVisible
          type="text"
          :disabled="isFetchingPF"
          :hint="dataPF ? 'Un identifiant a été automatiquement généré. Il est possible de le modifier.' : ''"
          autocomplete="off"
          spellcheck="false"
          @focus="prefillUsername"
          ref="usernameInput"
        />
      </DsfrInputGroup>
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'password')">
        <DsfrInput
          v-model="state.password"
          labelVisible
          :type="showPassword ? 'text' : 'password'"
          autocomplete="new-password"
          spellcheck="false"
        >
          <template #label>
            <div class="flex items-center justify-between">
              <div>Mot de passe</div>
              <PasswordDisplayToggle :showPassword="showPassword" @update:showPassword="showPassword = $event" />
            </div>
          </template>
        </DsfrInput>
        <PasswordRules />
      </DsfrInputGroup>
      <DsfrButton class="block! w-full!" :disabled="isFetching" label="Créer le compte" @click="submit" />
    </FormWrapper>
  </SingleItemWrapper>
</template>

<script setup>
import { computed, ref } from "vue"
import { useVuelidate } from "@vuelidate/core"
import SingleItemWrapper from "@/components/SingleItemWrapper"
import FormWrapper from "@/components/FormWrapper"
import { errorRequiredField, errorRequiredEmail, firstErrorMsg } from "@/utils/forms"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import { handleError } from "@/utils/error-handling"
import PasswordRules from "@/components/PasswordRules"
import PasswordDisplayToggle from "@/components/PasswordDisplayToggle"
import { useRoute, useRouter } from "vue-router"

const router = useRouter()
const route = useRoute()
const showPassword = ref(false)

// Form state & rules
const state = ref({
  lastName: route.query.firstName || "",
  firstName: route.query.lastName || "",
  email: route.query.email || "",
  username: "",
  password: "",
})

const rules = {
  lastName: errorRequiredField,
  firstName: errorRequiredField,
  email: errorRequiredEmail,
  username: errorRequiredField, // let back-end specify other errors (already taken),
  password: errorRequiredField, // let back-end specify other errors (length, rules)
}
const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

// Main request definition
const { data, response, execute, isFetching } = useFetch(
  "/api/v1/users/",
  {
    headers: headers(),
  },
  { immediate: false }
)
  .post(state)
  .json()

// Form validation

const submit = async () => {
  v$.value.$clearExternalResults()
  v$.value.$validate()
  if (v$.value.$error) {
    return // prevent API call if there is a front-end error
  }
  await execute()
  $externalResults.value = await handleError(response)
  if (response.value.ok) {
    router.push({ name: "VerificationSentPage", query: { email: state.value.email, userId: data.value.id } })
  }
}

// Username Pre-fill
const usernameInput = ref(null)
const urlPF = computed(
  () =>
    `/api/v1/generate-username?first_name=${encodeURIComponent(state.value.firstName)}&last_name=${encodeURIComponent(state.value.lastName)}`
)
const { data: dataPF, execute: executePF, isFetching: isFetchingPF } = useFetch(urlPF, {}, { immediate: false }).json()

const prefillUsername = async () => {
  if (state.value.firstName && state.value.lastName && !state.value.username) {
    await executePF()
    usernameInput.value.focus() // because the focus is lost as soon as the field is disabled when fetching
    if (dataPF.value) {
      state.value.username = dataPF.value.username
    }
  }
}
</script>
