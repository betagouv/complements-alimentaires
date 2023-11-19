<template>
  <div class="grid grid-cols-12">
    <div class="col-span-12 md:col-span-7 md:pr-10">
      <h3>S'abonner à l'info-lettre de veille réglementaire</h3>
      <div>Recevez tous les mois une actualisation réglementaire, des nouvelles de la plateforme teleicare....</div>
    </div>
    <div class="col-span-12 md:col-span-5 my-6 md:my-0">
      <DsfrInputGroup :error-message="errorMessage" :valid-message="validMessage">
        <div class="md:flex">
          <DsfrInput v-model="subscriptionEmail" :placeholder="placeholder" @keydown.enter="subscribe" />
          <DsfrButton class="mt-4 md:mt-0 md:ml-4" :disabled="requestInProgress" label="Valider" @click="subscribe" />
        </div>
      </DsfrInputGroup>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, email } from "@vuelidate/validators"

const placeholder = "Votre email"
const validMessage = ref()
const errorMessage = ref()
const requestInProgress = ref(false)
const subscriptionEmail = ref("")
const rules = computed(() => ({
  subscriptionEmail: { required, email },
}))
const v$ = useVuelidate(rules, { subscriptionEmail })

function subscribe() {
  v$.value.$validate()

  if (v$.value.$error) {
    errorMessage.value = "Ce champ doit contenir un email valide"
    validMessage.value = null
    return
  }

  const headers = {
    "X-CSRFToken": window.CSRF_TOKEN || "",
    "Content-Type": "application/json",
  }
  requestInProgress.value = true

  return fetch("/api/v1/subscribeNewsletter/", {
    method: "POST",
    headers,
    body: JSON.stringify({ email: subscriptionEmail.value }),
  })
    .then((response) => {
      if (response.ok) {
        errorMessage.value = null
        validMessage.value = "Votre subscription a bien été prise en compte"
      } else {
        errorMessage.value = "Une erreur est survenue, veuillez réessayer plus tard."
        validMessage.value = null
      }
    })
    .finally(() => {
      requestInProgress.value = false
    })
}
</script>
