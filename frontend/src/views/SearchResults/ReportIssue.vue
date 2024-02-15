<template>
  <div class="grid grid-cols-12">
    <div class="col-span-12 md:col-span-7 md:pr-10">
      <h3>Une erreur ? Signalez-là ici</h3>
      <p class="m-0">
        Aidez-nous à améliorer la qualité de nos données, en remontant toute erreur ou incohérence que vous pourriez
        constater. Nous vous remercions d'avance. 🙏🏼
      </p>
    </div>
    <div class="col-span-12 md:col-span-5 my-6 md:my-0">
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'email')">
        <DsfrInput v-model="state.email" placeholder="Votre email (optionnel)" />
      </DsfrInputGroup>
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'reportMessage')">
        <DsfrInput
          v-model="state.reportMessage"
          placeholder="Quel(s) problème(s) constatez-vous ?"
          :isTextarea="true"
          class="h-24"
        />
      </DsfrInputGroup>
      <div class="text-right">
        <DsfrButton :disabled="isFetching" label="Valider" @click="submit" />
      </div>
    </div>
  </div>
  <!-- <DsfrAlert title="titre" description="tout est ok" type="success" /> -->
</template>

<script setup>
import { reactive } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, email, helpers } from "@vuelidate/validators"
import { headers, firstErrorMsg } from "@/utils"
import { useFetch } from "@vueuse/core"

// Form state & rules
const state = reactive({
  email: "",
  reportMessage: "",
})
const rules = {
  email: { email: helpers.withMessage("Ce champ doit contenir un email valide", email) },
  reportMessage: { required: helpers.withMessage("Ce champ doit contenir vos constatations", required) },
}

const v$ = useVuelidate(rules, state)

// Request definition
const { data, error, execute, isFetching } = useFetch("/api/v1/reportIssue/", {
  headers: headers,
  immediate: false,
}).post(state)

// Form validation
const submit = () => {
  v$.value.$validate()
  if (v$.value.$error) {
    return // prevent API call if there is a front-end error
  }
  execute()

  if (error) {
    console.log(error.value)
  } else {
    console.log(data.value)
  }
}
</script>
