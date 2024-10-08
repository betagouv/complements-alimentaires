<template>
  <div>
    <div class="mb-4">
      <DsfrInputGroup>
        <div class="grid grid-cols-2 gap-6">
          <DsfrRadioButton
            v-for="category in decisionCategories"
            :key="category.value"
            v-model="decisionCategory"
            :value="category.value"
            name="decisionCategory"
            class="col-span-2 sm:col-span-1 !mb-0"
          >
            <template v-slot:label>
              <div class="font-bold">
                <v-icon :color="category.color" :name="category.icon" aria-hidden />
                {{ category.title }}
              </div>
              <p class="fr-text--sm !mb-0">
                {{ category.description }}
              </p>
            </template>
          </DsfrRadioButton>
        </div>
      </DsfrInputGroup>
    </div>
    <div v-if="decisionCategory === 'modify'" class="reject-reasons">
      <hr />
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'reasons')">
        <div class="mb-8" v-for="reason in rejectReasons" :key="reason.title">
          <p class="font-bold">{{ reason.title }}</p>
          <DsfrCheckboxSet
            v-model="reasons"
            :options="reason.items.map((x) => ({ label: x, name: x }))"
            :error-message="firstErrorMsg(v$, 'reason')"
          />
        </div>
      </DsfrInputGroup>
    </div>
    <div v-if="decisionCategory">
      <hr />
      <h3>Décision</h3>
      <DsfrHighlight>
        <template v-slot:default>
          <div class="sm:flex gap-4 mb-4">
            <div class="grow max-w-96">
              <DsfrInputGroup :error-message="firstErrorMsg(v$, 'proposal')">
                <DsfrSelect label="Proposition" v-model="proposal" :options="proposalOptions"></DsfrSelect>
              </DsfrInputGroup>
            </div>
            <div class="visa-checkbox content-end">
              <DsfrInputGroup>
                <DsfrCheckbox label="À viser" v-model="needsVisa" :disabled="disableVisaCheckbox" />
              </DsfrInputGroup>
            </div>
            <div class="content-end" v-if="decisionCategory != 'approve'">
              <DsfrInputGroup :error-message="firstErrorMsg(v$, 'delayDays')">
                <DsfrInput
                  :disabled="disableDelayDays"
                  v-model="delayDays"
                  label="Délai de réponse (jours)"
                  label-visible
                />
              </DsfrInputGroup>
            </div>
          </div>
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'comment')" v-if="decisionCategory != 'approve'">
            <DsfrInput
              is-textarea
              label-visible
              label="Motivation de la décision (à destination du professionnel)"
              v-model="comment"
            />
          </DsfrInputGroup>
          <DsfrButton class="" label="Soumettre" @click="submitDecision" />

          <div v-if="firstErrorMsg(v$, 'reasons')">{{ firstErrorMsg(v$, "reasons") }}</div>
        </template>
      </DsfrHighlight>
      <hr />
      <DsfrInputGroup>
        <DsfrInput
          v-model="privateNotes"
          is-textarea
          label-visible
          label="Notes de l'expert (à destination de l'administration)"
        />
      </DsfrInputGroup>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { helpers, required } from "@vuelidate/validators"
import { errorRequiredField, firstErrorMsg } from "@/utils/forms"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"
import { handleError } from "@/utils/error-handling"

const decisionCategory = ref(null)
watch(decisionCategory, () => (proposal.value = decisionCategory.value === "approve" ? "approve" : null))

const rules = computed(() => {
  if (decisionCategory.value !== "modify") return {}
  return {
    comment: errorRequiredField,
    reasons: { required: helpers.withMessage("Au moins une raison doit être selectionnée", required) },
    proposal: errorRequiredField,
    delayDays: proposal.value !== "rejection" ? errorRequiredField : {},
  }
})
const declaration = defineModel()
const proposal = ref(null)
const delayDays = ref(15)
const comment = ref("")
const reasons = ref([])
const privateNotes = ref(declaration.value?.privateNotes || "")

const $externalResults = ref({})
const v$ = useVuelidate(rules, { comment, proposal, reasons, delayDays }, { $externalResults })

const emit = defineEmits(["decision-done"])

const needsVisa = ref(false)
const mandatoryVisaProposals = ["objection", "rejection"]
const disableVisaCheckbox = computed(() => !proposal.value || mandatoryVisaProposals.indexOf(proposal.value) > -1)
const disableDelayDays = computed(() => proposal.value === "rejection")
watch(proposal, (newProposal) => {
  if (mandatoryVisaProposals.indexOf(newProposal) > -1) needsVisa.value = true
  if (newProposal === "objection") delayDays.value = 30
  else if (newProposal === "rejection") delayDays.value = null
  else delayDays.value = 15
})

const decisionCategories = [
  {
    value: "approve",
    title: "J’envoie l’attestation de déclaration",
    icon: "ri-checkbox-circle-fill",
    description: "La déclaration est conforme et peut être transmise.",
    color: "green",
  },
  {
    value: "modify",
    title: "Des changements sont nécessaires",
    icon: "ri-close-circle-fill",
    description: "La déclaration ne peut pas être transmise en l'état.",
    color: "red",
  },
]

const rejectReasons = [
  {
    title: "Le produit ne répond pas à la définition du complément alimentaire",
    items: [
      "Forme assimilable à un aliment courant",
      "Recommandations d'emploi incompatibles",
      "Composition (source concentrée, ...)",
      "Autre",
    ],
  },
  {
    title: "Le produit répond à la définition du médicament",
    items: ["Médicament par fonction", "Médicament par présentation", "Sevrage tabagique"],
  },
  {
    title: "Les procédures ne sont pas respectées",
    items: [
      "Présence d'un Novel Food",
      "Présence d'une forme d'apport en nutriments non autorisée",
      "Demande en article 17 attendue",
      "Demande en article 18 attendue",
    ],
  },
  {
    title: "Le dossier n'est pas recevable",
    items: [
      "Incohérences entre le dossier et l'étiquetage",
      "Informations manquantes",
      "Absence de preuve de reconnaissance mutuelle",
      "Absence ou non conformité de l'étiquetage",
      "Autre",
    ],
  },
  {
    title: "Le complément alimentaire n'est pas acceptable",
    items: ["Existence d'un risque"],
  },
]

const proposalOptions = computed(() => {
  if (decisionCategory.value === "approve") return [{ text: "Autorisation", value: "autorisation" }]

  return [
    { text: "Observation", value: "observation" },
    { text: "Objection", value: "objection" },
    { text: "Refus", value: "rejection" },
  ]
})

const submitDecision = async () => {
  v$.value.$reset()
  v$.value.$validate()
  if (v$.value.$error) {
    return
  }

  const actions = {
    observation: "observe",
    approve: "authorize",
    objection: "object",
    rejection: "reject",
  }
  const visaPath = needsVisa.value ? "with-visa" : "no-visa"
  const urlPath = `${actions[proposal.value]}-${visaPath}`

  const url = `/api/v1/declarations/${declaration.value?.id}/${urlPath}/`
  const { response } = await useFetch(url, { headers: headers() })
    .post({
      comment: comment.value,
      privateNotes: privateNotes.value,
      reasons: reasons.value,
      expiration: delayDays.value,
    })
    .json()
  $externalResults.value = await handleError(response)

  if (response.value.ok) {
    useToaster().addSuccessMessage("Votre décision a été prise en compte")
    emit("decision-done")
  }
}
</script>

<style scoped>
.reject-reasons:deep(.fr-input-group) {
  @apply !mb-0;
}
.visa-checkbox:deep(.fr-fieldset__element) {
  @apply !mb-1;
}
</style>
