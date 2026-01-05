<template>
  <div class="fr-container pb-10">
    <DsfrBreadcrumb :links="[{ to: '/', text: 'Accueil' }, { text: 'Contactez-nous' }]" />
    <h1>Contactez-nous</h1>
    <FormWrapper :externalResults="$externalResults">
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'name')">
        <DsfrInput class="max-w-md" v-model="state.name" label="Votre nom et prénom" required label-visible />
      </DsfrInputGroup>
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'email')">
        <DsfrInput class="max-w-md" v-model="state.email" label="Votre adresse email" required label-visible />
      </DsfrInputGroup>
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'message')">
        <DsfrInput class="max-w-2xl" isTextarea v-model="state.message" label="Message" required label-visible />
      </DsfrInputGroup>
      <div>
        <DsfrButton size="lg" icon="ri-mail-send-line" @click="sendEmail">
          Envoyer
          <span class="fr-sr-only">le message</span>
        </DsfrButton>
      </div>
    </FormWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useFetch } from "@vueuse/core"
import useToaster from "@/composables/use-toaster"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { useVuelidate } from "@vuelidate/core"
import FormWrapper from "@/components/FormWrapper"
import { firstErrorMsg } from "@/utils/forms"
import { errorRequiredField, errorRequiredEmail } from "@/utils/forms"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"
import { useRouter } from "vue-router"

const { loggedUser } = storeToRefs(useRootStore())
const router = useRouter()

const state = ref({
  name: "",
  email: "",
  message: "",
})

onMounted(() => {
  if (!loggedUser) return
  state.value.name = `${loggedUser.value.firstName} ${loggedUser.value.lastName}`
  state.value.email = loggedUser.value.email
})

const rules = {
  name: errorRequiredField,
  email: errorRequiredEmail,
  message: errorRequiredField,
}
const $externalResults = ref({})
const v$ = useVuelidate(rules, state, $externalResults)

const sendEmail = async () => {
  v$.value.$reset()
  v$.value.$validate()
  if (v$.value.$error) {
    return
  }
  const { response } = await useFetch("/api/v1/contact/", { headers: headers() }).post(state.value).json()
  $externalResults.value = await handleError(response)

  if (response.value.ok) {
    useToaster().addSuccessMessage("Le message a été envoyé et sera traité par notre équipe dans les plus brefs")
    router.push({ name: "Root" })
  }
}
</script>
