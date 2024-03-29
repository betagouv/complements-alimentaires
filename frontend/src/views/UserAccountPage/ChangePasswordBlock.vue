<template>
  <div>
    <SectionTitle title="Modifier mon mot de passe" icon="ri-shield-user-line" />
    <FormWrapper :externalResults="$externalResults">
      <div class="max-w-md">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'oldPassword')">
          <DsfrInput
            label="Ancien mot de passe"
            :type="showPasswords ? 'text' : 'password'"
            v-model="state.oldPassword"
            labelVisible
          />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'newPassword')">
          <DsfrInput
            label="Nouveau mot de passe"
            :type="showPasswords ? 'text' : 'password'"
            v-model="state.newPassword"
            labelVisible
          />
          <PasswordRules />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'newPasswordConfirm')">
          <DsfrInput
            label="Confirmez votre nouveau mot de passe"
            :type="showPasswords ? 'text' : 'password'"
            v-model="state.newPasswordConfirm"
            labelVisible
          />
        </DsfrInputGroup>
        <DsfrButton :disabled="isFetching" label="Modifier" @click="submit" size="sm" />
      </div>
    </FormWrapper>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useVuelidate } from "@vuelidate/core"
import SectionTitle from "@/components/SectionTitle"
import { headers } from "@/utils/data-fetching"
import { useFetch } from "@vueuse/core"
import FormWrapper from "@/components/FormWrapper"
import { errorRequiredField, firstErrorMsg } from "@/utils/forms"
import PasswordRules from "@/components/PasswordRules"

const showPasswords = ref(false)

// Form state & rules
const state = ref({
  oldPassword: "",
  newPassword: "",
  newPasswordConfirm: "",
})

const rules = {
  oldPassword: errorRequiredField,
  newPassword: errorRequiredField,
  newPasswordConfirm: errorRequiredField,
}

const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

// Request definition
const { data, response, execute, isFetching } = useFetch(
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
  v$.value.$validate()
  if (v$.value.$error) {
    return // prevent API call if there is a front-end error
  }
}
</script>
