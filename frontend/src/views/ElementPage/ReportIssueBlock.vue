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
        <DsfrInput
          label="Votre e-mail (optionnel)"
          labelVisible
          v-model="userEmail"
          type="email"
          autocomplete="email"
        />
      </DsfrInputGroup>
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'message')">
        <DsfrInput label="Quel(s) problème(s) constatez-vous ?" labelVisible v-model="message" :isTextarea="true" />
      </DsfrInputGroup>
      <div class="text-right">
        <DsfrButton :disabled="isFetching" label="Signaler l'erreur" @click="submit" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, email, helpers } from "@vuelidate/validators"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import { firstErrorMsg } from "@/utils/forms"
import useToaster from "@/composables/use-toaster"
import { useRootStore } from "@/stores/root"
import { handleError } from "@/utils/error-handling"
import { storeToRefs } from "pinia"

const props = defineProps({ element: Object, elementType: String })
const { loggedUser } = storeToRefs(useRootStore())
const message = ref("")
const userEmail = ref(loggedUser.value?.email || "")

// Form state & rules
const state = computed(() => {
  const nonIngredientTypes = ["substance", "microorganism", "plant"]
  const payloadType = nonIngredientTypes.indexOf(props.elementType) > -1 ? props.elementType : "ingredient"
  const initialState = { email: userEmail.value, message: message.value }
  initialState[payloadType] = props.element.id
  return initialState
})

const rules = {
  email: {
    email: helpers.withMessage("L'e-mail doit être en format valide (ex : nom@entreprise.com)", email),
  },
  message: { required: helpers.withMessage("Ce champ doit contenir vos constatations", required) },
}

const v$ = useVuelidate(rules, state)

// Request definition
const { response, execute, isFetching } = useFetch(
  "/api/v1/report-issue/",
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
  await handleError(response) // we don't get returned result as we don't except other errors than global
  if (response.value.ok) {
    useToaster().addMessage({
      type: "success",
      title: "C'est envoyé !",
      description: "Votre message a bien été envoyé. Merci pour votre contribution.",
    })
  }
  // Reset both form state & Vuelidate validation state
  message.value = ""
  v$.value.$reset()
}
</script>
