<template>
  <div>
    <div class="mb-6">
      <h3>Proposition à viser / signer</h3>
      <div class="border p-2">
        <VisaInfoLine title="Instructeur·ice" :text="instructorName" icon="ri-account-circle-line" />
        <VisaInfoLine
          title="Décision"
          icon="ri-focus-2-fill"
          :strikethroughText="hasOverridenOriginalDecision ? declarationProposal : ''"
          :text="hasOverridenOriginalDecision ? overridenProposal : declarationProposal"
        />
        <VisaInfoLine
          v-if="declaration.blockingReasons?.length"
          title="Raisons de la décision"
          icon="ri-edit-line"
          :strikethroughText="hasOverridenOriginalDecision ? declarationReasons : ''"
          :text="hasOverridenOriginalDecision ? overridenReasons : declarationReasons"
        />
        <VisaInfoLine
          title="Message au déclarant·e"
          icon="ri-chat-3-line"
          :strikethroughText="hasOverridenOriginalDecision ? declarationComment : ''"
          :text="hasOverridenOriginalDecision ? overridenComment : declarationComment"
        />
        <VisaInfoLine
          v-if="showExpirationDays"
          title="Délai de réponse"
          icon="ri-time-fill"
          :strikethroughText="hasOverridenOriginalDecision ? declarationExpirationDays : ''"
          :text="hasOverridenOriginalDecision ? overridenExpirationDays : declarationExpirationDays"
        />
        <div class="px-4 py-2 border bg-gray-50">
          <DecisionModificationModal v-model="overridenDecision" />
        </div>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-10">
      <div class="border p-4" v-for="decision in decisionCategories" :key="decision.title">
        <h6 class="font-bold">
          <v-icon :color="decision.iconColor" :name="decision.icon" scale="1.2" aria-hidden class="mr-1" />
          {{ decision.title }}
        </h6>
        <p class="fr-text--sm">
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

const $externalResults = ref({})
const emit = defineEmits(["decision-done"])
const declaration = defineModel()

const overridenDecision = ref()
const hasOverridenOriginalDecision = computed(
  () => overridenDecision.value && Object.keys(overridenDecision.value).length > 0
)

const producerMessage = ref(declaration.value.postValidationProducerMessage)

const instructorName = computed(() => {
  if (!declaration.value?.instructor) return "-"
  return `${declaration.value.instructor.firstName || ""} ${declaration.value.instructor.lastName || ""}`
})
const showExpirationDays = computed(
  () =>
    declaration.value.postValidationStatus === "OBJECTION" || declaration.value.postValidationStatus === "OBSERVATION"
)
const postValidationStatus = computed(() => statusProps[declaration.value.postValidationStatus].label)

const refusalUrl = computed(() => `/api/v1/declarations/${declaration.value.id}/refuse-visa/`)
const acceptanceUrl = computed(() => `/api/v1/declarations/${declaration.value.id}/accept-visa/`)
const postData = computed(() => ({ comment: producerMessage.value }))

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
      description: shouldBlockApproval.value
        ? "La déclaration ne peut pas être autorisée en nécessitant une saisine ANSEES."
        : "Je vise cette déclaration et signe.",
      buttonText: "Valider",
      buttonHandler: acceptVisa,
      blockedByAnses: shouldBlockApproval.value,
    },
    {
      title: "Je ne suis pas d'accord",
      icon: "ri-close-circle-fill",
      iconColor: "red",
      description: "Je renvoie le dossier en instruction.",
      buttonText: "Refuser",
      buttonHandler: refuseVisa,
    },
  ]
})

const declarationReasons = computed(() => declaration.value?.blockingReasons?.join(",\n"))
const overridenReasons = computed(() => overridenDecision.value?.reasons?.join(",\n"))

const declarationComment = computed(() => declaration.value?.postValidationProducerMessage)
const overridenComment = computed(() => overridenDecision.value?.comment)

const declarationExpirationDays = computed(() => declaration.value?.postValidationExpirationDays)
const overridenExpirationDays = computed(() => overridenDecision.value?.delayDays)

const declarationProposal = computed(() => postValidationStatus)
const overridenProposal = computed(() => statusProps[overridenDecision.value?.proposal]?.label)
</script>
