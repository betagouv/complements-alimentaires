<template>
  <div>
    <SectionTitle title="Voir et modifier mes informations personnelles" icon="ri-account-circle-line" />
    <div class="max-w-md">
      <FormWrapper :externalResults="$externalResults">
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
            autocomplete="username"
            spellcheck="false"
          />
        </DsfrInputGroup>
        <DsfrButton :disabled="isFetching" label="Modifier" @click="submit" size="sm" />
      </FormWrapper>
    </div>

    <DsfrModal
      :actions="actions"
      ref="modal"
      :opened="opened"
      @close="close"
      title="Votre compte va être désactivé"
      icon="ri-error-warning-line"
    >
      <p>
        Vous avez souhaité modifier votre adresse e-mail. Votre compte sera temporairement inutilisable, jusqu'à ce que
        vous confirmiez cette nouvelle adresse. Voulez-vous continuer ?
      </p>
    </DsfrModal>
  </div>
</template>

<script setup>
import SectionTitle from "@/components/SectionTitle"
import { computed, ref } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { useRootStore } from "@/stores/root"
import { headers } from "@/utils/data-fetching"
import { handleError } from "@/utils/error-handling"
import { useFetch } from "@vueuse/core"
import FormWrapper from "@/components/FormWrapper"
import { errorRequiredField, errorRequiredEmail, firstErrorMsg } from "@/utils/forms"
import { storeToRefs } from "pinia"
import { logOut } from "@/utils/auth"
import useToaster from "@/composables/use-toaster"

const store = useRootStore()
const { addSuccessMessage } = useToaster()
const { loggedUser } = storeToRefs(store)

// Form state & rules
const state = ref({
  lastName: loggedUser.value.lastName,
  firstName: loggedUser.value.firstName,
  email: loggedUser.value.email,
  username: loggedUser.value.username,
})

const rules = {
  lastName: errorRequiredField,
  firstName: errorRequiredField,
  email: errorRequiredEmail,
  username: errorRequiredField, // let back-end specify other errors (already taken),
}
const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

// Main request definition
const {
  data: userData,
  response,
  execute,
  isFetching,
} = useFetch(
  `/api/v1/users/${loggedUser.value.id}`,
  { headers: headers() },
  {
    immediate: false,
  }
)
  .put(state)
  .json()

// Form validation
const submit = async (displayWarning = true) => {
  v$.value.$clearExternalResults()
  v$.value.$validate()
  if (v$.value.$error) {
    return
  }
  close()
  if (displayWarning && emailHasChanged.value) {
    open()
    return
  }
  await execute()
  $externalResults.value = await handleError(response)
  if (response.value.ok) {
    const baseMessage = "Vos informations personnelles ont bien été modifiées."
    if (emailHasChanged.value) {
      await logOut(baseMessage, "VerificationSentPage", { userId: loggedUser.value.id, email: state.value.email })
    } else {
      addSuccessMessage(baseMessage)
    }
    store.setLoggedUser(userData.value)
  }
}

// Warning Modal
const opened = ref(false)
const emailHasChanged = computed(() => loggedUser.value.email != state.value.email)
const open = () => (opened.value = true)
const close = () => (opened.value = false)
const actions = [
  {
    label: "Modifier quand même",
    onClick: () => submit(false),
  },
  {
    label: "Annuler",
    onClick: close,
    secondary: true,
  },
]
</script>
