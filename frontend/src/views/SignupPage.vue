<template>
  <SingleItemWrapper>
    <h4>Se créer un compte</h4>
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
          autofocus
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
          autocomplete="off"
          spellcheck="false"
        >
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
        <div class="mt-1 fr-hint-text flex flex-col">
          <div>Votre mot de passe :</div>
          <DsfrBadge
            v-for="rule in passwordRules"
            :key="rule"
            :label="rule"
            class="!block !lowercase !bg-transparent !pl-0"
            small
            type="info"
          />
        </div>
      </DsfrInputGroup>
      <DsfrButton class="!block !w-full" :disabled="isFetching" label="Créer le compte" @click="submit" />
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
import { useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import useToaster from "@/composables/use-toaster"

const showPassword = ref(false)
const passwordRules = [
  "doit contenir au minimum 8 caractères",
  "ne peut pas être entièrement numérique",
  "ne peut pas trop ressembler à vos autres informations personnelles",
]

// Form state & rules
const state = ref({
  lastName: "",
  firstName: "",
  email: "",
  username: "",
  password: "",
})

const rules = {
  lastName: errorRequiredField,
  firstName: errorRequiredField,
  email: errorRequiredEmail,
  username: errorRequiredField, // let back-end specify other errors (length),
  password: errorRequiredField, // let back-end specify other errors (length, rules)
}
const router = useRouter()
const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

// Main request definition
const { response, execute, isFetching } = useFetch(
  "/api/v1/signup/",
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
    useToaster().addSuccessMessage("Votre compte utilisateur a bien été créé. Veuillez vous identifier avec.")
    router.push({ name: "LoginPage" })
  }
}

// Username Pre-fill
const usernameInput = ref(null)
const urlPF = computed(
  () => `/api/v1/generate-username?first_name=${state.value.firstName}&last_name=${state.value.lastName}`
)
const { data: dataPF, execute: executePF, isFetching: isFetchingPF } = useFetch(urlPF, {}, { immediate: false }).json()

const prefillUsername = async () => {
  if (state.value.firstName && state.value.lastName && !state.value.username) {
    await executePF()
    usernameInput.value.focus() // because the focus is lost when calling the endpoint
    if (dataPF.value) {
      state.value.username = dataPF.value.username
    }
  }
}
</script>
