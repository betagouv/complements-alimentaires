<template>
  <div>
    <div class="mb-6">
      <h3>Proposition à viser / signer</h3>
      <div class="border p-2">
        <VisaInfoLine title="Instructeur·ice" :text="instructorName" icon="ri-account-circle-line" />
        <VisaInfoLine title="Décision" :text="postValidationStatus" icon="ri-focus-2-fill" />
        <VisaInfoLine
          title="Message au déclarant·e"
          icon="ri-chat-3-line"
          :text="declaration.postValidationProducerMessage || '< sans commentaire >'"
        />
        <VisaInfoLine
          title="Délai de réponse"
          icon="ri-time-fill"
          :text="declaration.postValidationExpirationDays || '< non spécifié >'"
        />
      </div>
    </div>

    <DsfrInputGroup>
      <DsfrInput is-textarea label-visible label="Notes de l'expert (à destination de l'administration)" />
    </DsfrInputGroup>

    <div class="grid grid-cols-2 gap-10">
      <div class="border p-4" v-for="decision in decisionCategories" :key="decision.title">
        <h6 class="font-bold">
          <v-icon :color="decision.iconColor" :name="decision.icon" scale="1.2" aria-hidden class="mr-1" />
          {{ decision.title }}
        </h6>
        <p class="fr-text--sm">
          {{ decision.description }}
        </p>
        <div class="text-right">
          <DsfrButton :label="decision.buttonText" @click="decision.buttonHandler" secondary />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { statusProps } from "@/utils/mappings"
import VisaInfoLine from "./VisaInfoLine.vue"

const props = defineProps({ declaration: Object })

const decisionCategory = ref(null)
watch(decisionCategory, () => (proposal.value = decisionCategory.value === "approve" ? "approve" : null))

const proposal = ref(null)

const needsVisa = ref(false)
const mandatoryVisaProposals = ["objection", "rejection"]
watch(proposal, (newProposal) => {
  if (mandatoryVisaProposals.indexOf(newProposal) > -1) needsVisa.value = true
})

const instructorName = computed(
  () => `${props.declaration?.instructor?.firstName} ${props.declaration?.instructor?.lastName}`
)
const postValidationStatus = computed(() => statusProps[props.declaration.postValidationStatus].label)
const decisionCategories = computed(() => {
  return [
    {
      title: "Je valide cette décision",
      icon: "ri-checkbox-circle-fill",
      iconColor: "green",
      description: `Je suis d'accord pour donner mon visa et signature. La déclaration partirà en état «
          ${postValidationStatus.value} ».`,
      buttonText: "Valider",
      buttonHandler: null,
    },
    {
      title: "Je ne suis pas d'accord",
      icon: "ri-close-circle-fill",
      iconColor: "red",
      description: `Je ne donne pas mon visa ni signature. La déclaration repartirà en instruction chez
          ${instructorName.value}.`,
      buttonText: "Refuser",
      buttonHandler: null,
    },
  ]
})
</script>
