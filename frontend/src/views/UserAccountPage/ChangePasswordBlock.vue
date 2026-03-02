<template>
  <div>
    <SectionTitle title="Modifier mon mot de passe" icon="ri-shield-user-line" />
    <div class="max-w-md">
      <FormWrapper :externalResults="$externalResults">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'oldPassword')">
          <DsfrInput
            label="Ancien mot de passe"
            :type="showPassword ? 'text' : 'password'"
            v-model="state.oldPassword"
            labelVisible
            autocomplete="current-password"
          />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'newPassword')">
          <DsfrInput
            label="Nouveau mot de passe"
            :type="showPassword ? 'text' : 'password'"
            v-model="state.newPassword"
            labelVisible
            autocomplete="new-password"
          />
          <PasswordRules />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'confirmNewPassword')">
          <DsfrInput
            label="Confirmez votre nouveau mot de passe"
            :type="showPassword ? 'text' : 'password'"
            v-model="state.confirmNewPassword"
            labelVisible
            autocomplete="new-password"
          />
        </DsfrInputGroup>
        <div class="flex justify-between">
          <DsfrButton :disabled="isFetching" label="Modifier" @click="submit" size="sm" />
          <PasswordDisplayToggle
            manyPasswords
            :showPassword="showPassword"
            @update:showPassword="showPassword = $event"
          />
        </div>
      </FormWrapper>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useVuelidate } from "@vuelidate/core"
import SectionTitle from "@/components/SectionTitle"
import { headers } from "@/utils/data-fetching"
import { handleError } from "@/utils/error-handling"
import { useFetch } from "@vueuse/core"
import FormWrapper from "@/components/FormWrapper"
import { errorRequiredField, firstErrorMsg } from "@/utils/forms"
import PasswordRules from "@/components/PasswordRules"
import PasswordDisplayToggle from "@/components/PasswordDisplayToggle"
import { logOut } from "@/utils/auth"

const showPassword = ref(false)

// Form state & rules
const getInitialState = () => ({
  oldPassword: "",
  newPassword: "",
  confirmNewPassword: "",
})

const state = ref(getInitialState())

const rules = {
  oldPassword: errorRequiredField,
  newPassword: errorRequiredField,
  confirmNewPassword: errorRequiredField,
}

const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

// Request definition
const { response, execute, isFetching } = useFetch(
  "/api/v1/change-password/",
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
    // Logout is not really necessary but Django removes session id from front-end after a change password
    await logOut("Votre mot de passe a bien été modifié. Veuillez vous reconnecter.", "LoginPage")
  }
}
</script>
