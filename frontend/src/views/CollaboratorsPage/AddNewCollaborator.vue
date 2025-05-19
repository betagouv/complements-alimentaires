<template>
  <div>
    <DsfrButton @click="opened = true" label="Ajouter un collaborateur" icon="ri-user-add-line" size="sm" />
    <DsfrModal
      :actions="actions"
      ref="modal"
      :opened="opened"
      @close="close"
      title="Ajouter un collaborateur"
      icon="ri-user-add-line"
    >
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'recipientEmail')">
        <DsfrInput
          v-model="state.recipientEmail"
          label="Entrez l'adresse e-mail de votre collaborateur :"
          labelVisible
          type="email"
          autocomplete="email"
          spellcheck="false"
          class="max-w-md"
        />
      </DsfrInputGroup>
      <DsfrCheckboxSet
        :error-message="firstErrorMsg(v$, 'selectedRoles')"
        v-model="state.selectedRoles"
        :options="selectableRoles"
        small
        legend="Sélectionnez un ou plusieurs rôles qui lui seront attribués :"
      />
    </DsfrModal>
  </div>
</template>

<script setup>
import { ref } from "vue"
import useVuelidate from "@vuelidate/core"
import { useFetch } from "@vueuse/core"
import useToaster from "@/composables/use-toaster"
import { errorRequiredField, errorRequiredEmail, firstErrorMsg } from "@/utils/forms"
import { roleNameDisplayNameMapping } from "@/utils/mappings"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"

const emit = defineEmits(["added"])
const opened = ref(false)
const props = defineProps({ companyId: Number })

// Form state & rules

const getInitialState = () => ({
  recipientEmail: "",
  selectedRoles: [],
})

const state = ref(getInitialState())

const rules = {
  recipientEmail: errorRequiredEmail,
  selectedRoles: errorRequiredField,
}

const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

const selectableRoles = [
  {
    label: roleNameDisplayNameMapping.DeclarantRole,
    value: "DeclarantRole",
    hint: "permet au collaborateur de créer et gérer ses propres déclarations.",
  },
  {
    label: roleNameDisplayNameMapping.SupervisorRole,
    value: "SupervisorRole",
    hint: "permet au collaborateur de gérer l'ensemble de l'entreprise (les déclarations existantes, les collaborateurs, et l'entreprise elle-même).",
  },
]

const close = () => {
  // Remet à zéro le form state et le Vuelidate validation state
  opened.value = false
  state.value = getInitialState()
  v$.value.$reset()
}

const submit = async () => {
  v$.value.$clearExternalResults()
  v$.value.$validate()
  if (v$.value.$error) {
    return
  }
  const url = `/api/v1/companies/${props.companyId}/add-new-collaborator/`
  const { response, data } = await useFetch(url, { headers: headers() })
    .post({ roles: state.value.selectedRoles, recipientEmail: state.value.recipientEmail })
    .json()
  $externalResults.value = await handleError(response)
  if (response.value.ok) {
    emit("added")
    useToaster().addMessage({
      type: "success",
      // exceptionnellement on utilise le message directement du back, car plusieurs cas possibles
      description: data.value.message,
    })
    close()
  }
}

const actions = [
  {
    label: "Valider",
    onClick: submit,
  },
  {
    label: "Annuler",
    onClick: close,
    secondary: true,
  },
]
</script>
