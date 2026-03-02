<template>
  <div class="grid grid-cols-12">
    <div class="col-span-12 md:col-span-7 md:pr-10">
      <h3>S'abonner à l'info-lettre de veille réglementaire</h3>
      <p class="m-0">Il sera bientôt possible de recevoir des mises à jour sur les actualités réglementaires</p>
    </div>
    <div class="col-span-12 md:col-span-5 my-6 md:my-0">
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'email')">
        <div class="md:flex justify-between items-end">
          <div class="grow">
            <DsfrInput
              v-model="state.email"
              label="Votre e-mail"
              labelVisible
              @keydown.enter="submit"
              type="email"
              autocomplete="email"
            />
          </div>
          <DsfrButton class="mt-4 md:mt-0 md:ml-4" :disabled="isFetching" @click="submit">
            S'abonner
            <span class="fr-sr-only">à l'info-lettre</span>
          </DsfrButton>
        </div>
      </DsfrInputGroup>
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
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"

// Get potential existing user from root store to pre-fill email address
const store = useRootStore()
const { loggedUser } = storeToRefs(store)

// Form state & rules
const state = ref({ email: loggedUser.value ? loggedUser.value.email : "" })

const rules = {
  email: errorRequiredEmail,
}

const v$ = useVuelidate(rules, state)

// Request definition
const { response, execute, isFetching } = useFetch(
  "/api/v1/subscribe-newsletter/",
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
  await handleError(response)

  const { addSuccessMessage } = useToaster()
  if (response.value.ok) {
    addSuccessMessage("Votre inscription a bien été prise en compte.")
    // Reset both form state & Vuelidate validation state
    state.value.email = ""
    v$.value.$reset()
  }
}
</script>
