<template>
  <div class="grid grid-cols-12">
    <div class="col-span-12 md:col-span-7 md:pr-10">
      <h3>S'abonner à l'info-lettre de veille réglementaire</h3>
      <p class="m-0">
        Recevez tous les mois une actualisation réglementaire, des nouvelles de la plateforme teleicare....
      </p>
    </div>
    <div class="col-span-12 md:col-span-5 my-6 md:my-0">
      <FormWrapper :externalResults="$externalResults">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'email')">
          <div class="md:flex justify-between items-end">
            <div class="grow">
              <DsfrInput v-model="state.email" label="Votre e-mail" labelVisible @keydown.enter="submit" />
            </div>
            <DsfrButton class="mt-4 md:mt-0 md:ml-4" :disabled="isFetching" label="Valider" @click="submit" />
          </div>
        </DsfrInputGroup>
      </FormWrapper>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { headers } from "@/utils/data-fetching"
import { errorRequiredEmail, firstErrorMsg } from "@/utils/forms"
import { useFetch } from "@vueuse/core"
import useToaster from "@/composables/use-toaster"
import { handleError } from "@/utils/error-handling"
import FormWrapper from "@/components/FormWrapper"
import { useRootStore } from "@/stores/root"

// Get potential existing user from root store to pre-fill email address
const { loggedUser } = useRootStore()

// Form state & rules
const state = ref({ email: loggedUser ? loggedUser.email : "" })

const rules = {
  email: errorRequiredEmail,
}

const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

// Request definition
const { error, response, execute, isFetching } = useFetch(
  "/api/v1/subscribeNewsletter/",
  {
    headers: headers(),
  },
  { immediate: false }
).post(state)

// Form validation
const submit = async () => {
  v$.value.$validate()
  if (v$.value.$error) {
    return // prevent API call if there is a front-end error
  }
  await execute()
  $externalResults.value = await handleError(response, error)

  const { addMessage } = useToaster()
  if (!error.value) {
    addMessage({
      type: "success",
      title: "C'est tout bon !",
      description: "Votre inscription a bien été prise en compte.",
    })
    // Reset both form state & Vuelidate validation state
    state.value.email = ""
    v$.value.$reset()
  }
}
</script>
