<template>
  <div>
    <DsfrAlert>
      L'entreprise
      <strong>{{ company.socialName }}</strong>
      avec le n° {{ company.identifierType.toUpperCase() + " " }}
      <strong>{{ company.identifier }}</strong>
      existe déjà dans Compl-Alim. Vous pouvez cependant envoyer une demande d'accès aux gestionnaires.

      <DsfrInputGroup>
        <DsfrCheckbox
          :hint="`Vous avec déjà des droits de déclaration sur la compagnie ${company.socialName}`"
          label="Demander les droits de déclaration"
          checked
          disabled
          v-if="hasDeclarationRole"
        />
        <DsfrCheckbox
          hint="Cochez cette case pour créer des dossier et déclarations au nom de cette entreprise"
          v-model="declarantRole"
          label="Demander les droits de déclaration"
          v-else
        />
        <DsfrCheckbox
          hint="Cochez cette pour avoir la gestion des rôles, déclarations et informations de l'entreprise"
          v-model="supervisorRole"
          label="Demander les droits de supervision"
        />
      </DsfrInputGroup>

      <DsfrInputGroup>
        <DsfrInput v-model="message" label="Message (optionnel)" labelVisible isTextarea />
      </DsfrInputGroup>

      <div class="flex gap-x-4">
        <DsfrButton
          label="Demander l'accès"
          icon="ri-key-2-line"
          @click="submitClaimCompanyAccess"
          :disabled="isFetching"
        />
      </div>
    </DsfrAlert>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { useRootStore } from "@/stores/root"
import { useFetch } from "@vueuse/core"
import { useVuelidate } from "@vuelidate/core"
import { headers } from "@/utils/data-fetching"
import { handleError } from "@/utils/error-handling"

const store = useRootStore()

// Props & emits
const company = defineModel()
const emit = defineEmits(["changeStep"])

// Form state & rules
const message = ref("")
const declarantRole = ref(true)
const supervisorRole = ref(false)

const $externalResults = ref({})
const v$ = useVuelidate({}, { message: message }, { $externalResults })

const hasDeclarationRole = computed(() =>
  store.loggedUser.companies?.find((x) => x.id === company.value.id)?.roles?.find((x) => x.name === "DeclarantRole")
)

// Request definition
const url = computed(() => `/api/v1/companies/${company.value.id}/claim-company-access/`)
const { response, execute, isFetching } = useFetch(
  url,
  {
    headers: headers(),
  },
  { immediate: false }
)
  .post(() => ({
    message: message.value,
    declarantRole: declarantRole.value,
    supervisorRole: supervisorRole.value,
  }))
  .json()

// Request execution
const submitClaimCompanyAccess = async () => {
  v$.value.$validate()
  // pas besoin de vérifier les erreurs fronts, car pas possible sur le seul champ message
  await execute()
  $externalResults.value = await handleError(response)
  if (response.value.ok) {
    emit("changeStep", {
      name: `Demande d'accès effectuée`,
      component: "EndClaimDone",
    })
  }
}
</script>
