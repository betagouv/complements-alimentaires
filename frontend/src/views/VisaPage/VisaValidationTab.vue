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
      <DsfrInput
        v-model="privateNotes"
        is-textarea
        label-visible
        label="Notes de l'expert (à destination de l'administration)"
      />
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
import { ref, computed } from "vue"
import { statusProps } from "@/utils/mappings"
import { headers } from "@/utils/data-fetching"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import useToaster from "@/composables/use-toaster"
import VisaInfoLine from "./VisaInfoLine.vue"

const $externalResults = ref({})
const emit = defineEmits(["decision-done"])
const declaration = defineModel()

const privateNotes = ref(declaration.value?.privateNotes || "")

const instructorName = computed(
  () => `${declaration.value?.instructor?.firstName} ${declaration.value?.instructor?.lastName}`
)
const postValidationStatus = computed(() => statusProps[declaration.value.postValidationStatus].label)
const refuseVisa = async () => {
  const url = `/api/v1/declarations/${declaration.value.id}/refuse-visa/`
  const { response } = await useFetch(url, { headers: headers() }).post({ privateNotes: privateNotes.value }).json()
  $externalResults.value = await handleError(response)
  if (response.value.ok) {
    useToaster().addSuccessMessage("Votre décision a été prise en compte")
    emit("decision-done")
  }
}

const acceptVisa = async () => {
  const url = `/api/v1/declarations/${declaration.value.id}/accept-visa/`
  const { response } = await useFetch(url, { headers: headers() }).post({ privateNotes: privateNotes.value }).json()
  $externalResults.value = await handleError(response)
  if (response.value.ok) {
    useToaster().addSuccessMessage("Votre décision a été prise en compte")
    emit("decision-done")
  }
}

const decisionCategories = computed(() => {
  return [
    {
      title: "Je valide cette décision",
      icon: "ri-checkbox-circle-fill",
      iconColor: "green",
      description: "Je vise cette déclaration et signe.",
      buttonText: "Valider",
      buttonHandler: acceptVisa,
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
</script>
