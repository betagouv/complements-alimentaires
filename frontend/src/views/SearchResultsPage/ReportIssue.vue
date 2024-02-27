<template>
  <div class="grid grid-cols-12">
    <div class="col-span-12 md:col-span-7 md:pr-10">
      <h4>Une erreur ? Signalez-là ici</h4>
      <p class="m-0">
        Aidez-nous à améliorer la qualité de nos données en remontant toute erreur ou incohérence que vous pourriez
        constater. Nous vous remercions d'avance 🙏🏼
      </p>
    </div>
    <div class="col-span-12 md:col-span-5 my-6 md:my-0">
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'email')">
        <DsfrInput v-model="state.email" placeholder="Votre e-mail (optionnel)" />
      </DsfrInputGroup>
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'reportMessage')">
        <DsfrInput
          v-model="state.reportMessage"
          placeholder="Quel(s) problème(s) constatez-vous ?"
          :isTextarea="true"
        />
      </DsfrInputGroup>
      <div class="text-right">
        <DsfrButton :disabled="isFetching" label="Valider" @click="submit" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, email, helpers } from "@vuelidate/validators"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import { firstErrorMsg } from "@/utils/forms"
import useToaster from "@/composables/use-toaster"

// Props
const props = defineProps({ elementName: String })

// Form state & rules
const getInitialState = () => ({
  name: "",
  email: "",
  elementName: props.elementName, // not used by the form validation itself, but make the payload building easier
})

const state = ref(getInitialState())

const rules = {
  email: { email: helpers.withMessage("Ce champ doit contenir un e-mail valide s'il est spécifié", email) },
  reportMessage: { required: helpers.withMessage("Ce champ doit contenir vos constatations", required) },
}

const v$ = useVuelidate(rules, state)

// Request definition
const { error, execute, isFetching } = useFetch(
  "/api/v1/reportIssue/",
  {
    headers: headers,
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

  const { addMessage, addUnknownErrorMessage } = useToaster()
  if (error.value) {
    addUnknownErrorMessage()
  } else {
    addMessage({
      type: "success",
      title: "C'est envoyé !",
      description: "Votre message a bien été envoyé. Merci pour votre contribution.",
    })
  }
  // Reset both form state & Vuelidate validation state
  state.value = getInitialState()
  v$.value.$reset()
}
</script>
