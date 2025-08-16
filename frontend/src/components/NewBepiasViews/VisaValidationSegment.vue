<template>
  <div>
    <div v-if="readonly">
      <p>Cette déclaration est actuellement en état « {{ statusProps[declaration.status].label }} ».</p>
    </div>
    <div v-else>
      <div class="mb-6">
        <div class="border p-2">
          <VisaInfoLine title="Instructeur·ice" :text="instructorName" icon="ri-account-circle-line" />
          <VisaInfoLine
            title="Décision"
            icon="ri-focus-2-fill"
            :strikethroughText="hasOverriddenOriginalDecision ? declarationProposal : ''"
            :text="hasOverriddenOriginalDecision ? overriddenProposal : declarationProposal"
          />
          <VisaInfoLine
            v-if="hasOverriddenOriginalDecision ? overriddenReasons : declarationReasons"
            title="Raisons de la décision"
            icon="ri-edit-line"
            :strikethroughText="hasOverriddenOriginalDecision ? declarationReasons : ''"
            :text="hasOverriddenOriginalDecision ? overriddenReasons : declarationReasons"
          />
          <VisaInfoLine
            title="Message au déclarant·e"
            icon="ri-chat-3-line"
            :strikethroughText="hasOverriddenOriginalDecision ? declarationComment : ''"
            :text="hasOverriddenOriginalDecision ? overriddenComment : declarationComment"
          />
          <VisaInfoLine
            v-if="showExpirationDays"
            title="Délai de réponse"
            icon="ri-time-fill"
            :strikethroughText="hasOverriddenOriginalDecision ? declarationExpirationDays : ''"
            :text="hasOverriddenOriginalDecision ? overriddenExpirationDays : declarationExpirationDays"
          />
          <div class="px-4 py-2 border bg-gray-50">
            <DecisionModificationModal v-model="overriddenDecision" />
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-10">
        <div class="border p-4 flex flex-col" v-for="decision in decisionCategories" :key="decision.title">
          <h6 class="font-bold">
            <v-icon :color="decision.iconColor" :name="decision.icon" scale="1.2" aria-hidden class="mr-1" />
            {{ decision.title }}
          </h6>
          <p class="fr-text--sm grow">
            {{ decision.description }}
          </p>
          <ArticleInfoRow class="mb-2" v-if="decision.blockedByAnses" v-model="declaration" />
          <div v-else class="text-right">
            <DsfrButton
              :label="decision.buttonText"
              @click="decision.buttonHandler"
              secondary
              :disabled="refuseIsFetching || acceptIsFetching || decision.blockedByAnses"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { statusProps } from "@/utils/mappings"
import { headers } from "@/utils/data-fetching"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import useToaster from "@/composables/use-toaster"
import VisaInfoLine from "./VisaInfoLine.vue"
import ArticleInfoRow from "@/components/DeclarationSummary/ArticleInfoRow"
import DecisionModificationModal from "./DecisionModificationModal"
import { useStorage } from "@vueuse/core"

const getLocalStorageKey = (key) => `visa-${declaration.value?.id}-${key}`
const clearLocalStorage = () => {
  const keys = ["overriddenDecision"]
  for (const key of keys) localStorage.removeItem(getLocalStorageKey(key))
}

const $externalResults = ref({})
const emit = defineEmits(["decision-done"])
const declaration = defineModel()
defineProps({ readonly: Boolean })

const overriddenDecision = useStorage(getLocalStorageKey("overriddenDecision"), null, undefined, {
  serializer: {
    read: (v) => (v ? JSON.parse(v) : null),
    write: (v) => JSON.stringify(v),
  },
})
const hasOverriddenOriginalDecision = computed(
  () => overriddenDecision.value && Object.keys(overriddenDecision.value).length > 0
)

const instructorName = computed(() => {
  if (!declaration.value?.instructor) return "-"
  return `${declaration.value.instructor.firstName || ""} ${declaration.value.instructor.lastName || ""}`
})
const showExpirationDays = computed(() => {
  const concernedStatuses = ["OBJECTION", "OBSERVATION"]
  const validationStatus = hasOverriddenOriginalDecision.value
    ? overriddenDecision.value.proposal
    : declaration.value.postValidationStatus
  return concernedStatuses.indexOf(validationStatus) > -1
})
const postValidationStatus = computed(() => statusProps[declaration.value.postValidationStatus].label)

const refusalUrl = computed(() => `/api/v1/declarations/${declaration.value.id}/refuse-visa/`)
const acceptanceUrl = computed(() => `/api/v1/declarations/${declaration.value.id}/accept-visa/`)
const postData = computed(() => overriddenDecision.value || {})

const {
  execute: refuseExecute,
  isFetching: refuseIsFetching,
  response: refuseResponse,
} = useFetch(refusalUrl, { headers: headers() }, { immediate: false }).post(postData).json()
const {
  execute: acceptExecute,
  isFetching: acceptIsFetching,
  response: acceptResponse,
} = useFetch(acceptanceUrl, { headers: headers() }, { immediate: false }).post(postData).json()

const refuseVisa = async () => {
  await refuseExecute()
  $externalResults.value = await handleError(refuseResponse)
  if (refuseResponse.value.ok) notifySuccess()
}

const acceptVisa = async () => {
  await acceptExecute()
  $externalResults.value = await handleError(acceptResponse)
  if (acceptResponse.value.ok) notifySuccess()
}

const notifySuccess = () => {
  useToaster().addSuccessMessage("Votre décision a été prise en compte")
  clearLocalStorage()
  emit("decision-done")
}

const needsAnsesReferal = computed(() => declaration.value?.article === "ANSES_REFERAL")
const shouldBlockApproval = computed(
  () => needsAnsesReferal.value && declaration.value.postValidationStatus === "AUTHORIZED"
)
const decisionCategories = computed(() => {
  return [
    {
      title: "Je valide cette décision",
      icon: "ri-checkbox-circle-fill",
      iconColor: "green",
      description: validationHelperText.value,
      buttonText: "Valider",
      buttonHandler: acceptVisa,
      blockedByAnses: shouldBlockApproval.value,
    },
    {
      title: "Je ne suis pas d'accord",
      icon: "ri-close-circle-fill",
      iconColor: "red",
      description: refusalHelperText.value,
      buttonText: "Refuser",
      buttonHandler: refuseVisa,
    },
  ]
})

const validationHelperText = computed(() => {
  if (shouldBlockApproval.value) return "La déclaration ne peut pas être autorisée en nécessitant une saisine ANSES."
  if (hasOverriddenOriginalDecision.value)
    return "Je vise cette déclaration avec les modifications effectuées et signe."
  return "Je vise cette déclaration et signe."
})

const refusalHelperText = computed(() => {
  if (hasOverriddenOriginalDecision.value)
    return "Je renvoie le dossier en instruction. Les modifications effectuées ne seront pas prises en compte."
  return "Je renvoie le dossier en instruction."
})

const declarationReasons = computed(() => declaration.value?.blockingReasons?.join(",\n"))
const overriddenReasons = computed(() => overriddenDecision.value?.reasons?.join(",\n"))

const declarationComment = computed(() => declaration.value?.postValidationProducerMessage)
const overriddenComment = computed(() => overriddenDecision.value?.comment)

const declarationExpirationDays = computed(() => declaration.value?.postValidationExpirationDays)
const overriddenExpirationDays = computed(() => overriddenDecision.value?.delayDays)

const declarationProposal = computed(() => postValidationStatus)
const overriddenProposal = computed(() => statusProps[overriddenDecision.value?.proposal]?.label)
</script>
