<template>
  <div>
    <div v-if="readonly">
      <p>Cette déclaration est actuellement en état « {{ statusProps[declaration.status].label }} ».</p>
    </div>
    <div v-else>
      <h3 class="fr-h4" id="decision">Décision</h3>
      <div class="mb-4">
        <DsfrInputGroup>
          <DsfrRadioButton
            v-for="category in decisionCategories"
            :key="category.value"
            v-model="decisionCategory"
            :value="category.value"
            name="decisionCategory"
          >
            <template v-slot:label>
              <div>
                <v-icon :color="category.color" :name="category.icon" aria-hidden />
                {{ category.title }}
              </div>
            </template>
          </DsfrRadioButton>
        </DsfrInputGroup>
      </div>

      <div v-if="decisionCategory === 'modify'" class="mb-4 mt-8">
        <h3 class="fr-h4" id="justification">Justification de la contestation</h3>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'reasons')">
          <DsfrMultiselect
            label="Raisons de contestation"
            v-model="reasons"
            :options="blockingReasons.flatMap((x) => x.items)"
            :required="true"
            :search="true"
            :button-label="reasons?.length ? reasons.join(', ') : 'Sélectionner une option'"
          />
        </DsfrInputGroup>
        <div class="sm:flex gap-4 changes-needed-fields">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'proposal')">
            <DsfrSelect label="Proposition" v-model="proposal" :options="proposalOptions"></DsfrSelect>
          </DsfrInputGroup>
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'delayDays')">
            <DsfrInput
              :disabled="disableDelayDays"
              v-model="delayDays"
              label="Délai de réponse (jours)"
              label-visible
            />
          </DsfrInputGroup>
        </div>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'comment')">
          <DsfrInput
            is-textarea
            label-visible
            label="Motivation de la décision (à destination du professionnel)"
            v-model="comment"
          />
        </DsfrInputGroup>
      </div>

      <div
        v-if="decisionCategory && !(needsAnsesReferal && decisionCategory === 'approve')"
        class="flex items-center decision-action p-2 border rounded"
      >
        <DsfrInputGroup class="mb-0">
          <DsfrCheckbox label="À viser" v-model="needsVisa" :disabled="disableVisaCheckbox" />
        </DsfrInputGroup>
        <div class="border-l ml-4 pl-4">
          <DsfrButton
            label="Soumettre"
            @click="submitDecision"
            :disabled="isFetching || (needsAnsesReferal && decisionCategory === 'approve')"
          />
        </div>
      </div>

      <div v-if="needsAnsesReferal && decisionCategory === 'approve'" class="mt-2">
        <hr class="p-0 my-2" />
        <p class="my-1">
          <v-icon name="ri-error-warning-line"></v-icon>
          La déclaration ne peut pas être validée en nécessitant une saisine ANSES. Merci de changer l'article avant de
          la valider.
        </p>
        <ArticleInfoRow
          v-model="declaration"
          v-if="needsAnsesReferal && decisionCategory === 'approve'"
          :allowChange="true"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { helpers, required } from "@vuelidate/validators"
import { errorRequiredField, errorInteger, firstErrorMsg } from "@/utils/forms"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"
import { handleError } from "@/utils/error-handling"
import ArticleInfoRow from "@/components/DeclarationSummary/ArticleInfoRow"
import { blockingReasons } from "@/utils/mappings"
import { statusProps } from "@/utils/mappings"
import { useRouter } from "vue-router"
import { useStorage } from "@vueuse/core"

const router = useRouter()

const rules = computed(() => {
  if (decisionCategory.value !== "modify") return {}
  return {
    comment: errorRequiredField,
    reasons: { required: helpers.withMessage("Au moins une raison doit être selectionnée", required) },
    proposal: errorRequiredField,
    delayDays: proposal.value !== "rejection" ? Object.assign({}, errorRequiredField, errorInteger) : {},
  }
})
const declaration = defineModel()
defineProps({ readonly: Boolean })

const getLocalStorageKey = (key) => `instruction-${declaration.value?.id}-${key}`

const clearLocalStorage = () => {
  const keys = ["proposal", "delayDays", "comment", "reasons", "decisionCategory", "needsVisa"]
  for (const key of keys) localStorage.removeItem(getLocalStorageKey(key))
}

const proposal = useStorage(getLocalStorageKey("proposal"), null)
const delayDays = useStorage(getLocalStorageKey("delayDays"), null)
const comment = useStorage(getLocalStorageKey("comment"), declaration.value?.lastAdministrationComment || "")
const reasons = useStorage(getLocalStorageKey("reasons"), [])
const decisionCategory = useStorage(getLocalStorageKey("decisionCategory"), null)
const needsVisa = useStorage(getLocalStorageKey("needsVisa"), false)

watch(decisionCategory, () => (proposal.value = decisionCategory.value === "approve" ? "autorisation" : null))

const $externalResults = ref({})
const v$ = useVuelidate(rules, { comment, proposal, reasons, delayDays }, { $externalResults })

const decisionCategories = [
  {
    icon: "ri-checkbox-circle-fill",
    color: "green",
    value: "approve",
    title: "Approbation : la déclaration est conforme.",
  },
  {
    icon: "ri-close-circle-fill",
    color: "red",
    value: "modify",
    title: "Des changements sont nécessaires : la déclaration n’est pas finalisée.",
  },
]

const mandatoryVisaProposals = ["objection", "rejection"]
const disableVisaCheckbox = computed(() => !proposal.value || mandatoryVisaProposals.indexOf(proposal.value) > -1)
const disableDelayDays = computed(() => proposal.value === "rejection")
watch(proposal, (newProposal) => {
  if (mandatoryVisaProposals.indexOf(newProposal) > -1) needsVisa.value = true
  else needsVisa.value = false
  if (newProposal === "objection") delayDays.value = 30
  else if (newProposal === "observation") delayDays.value = window.OBSERVATION_DAYS
  else delayDays.value = null
})

const needsAnsesReferal = computed(() => declaration.value?.article === "ANSES_REFERAL")

const proposalOptions = [
  { text: "Observation", value: "observation" },
  { text: "Objection", value: "objection" },
  { text: "Refus", value: "rejection" },
]

const url = computed(() => {
  const actions = {
    observation: "observe",
    autorisation: "authorize",
    objection: "object",
    rejection: "reject",
  }
  const visaPath = needsVisa.value ? "with-visa" : "no-visa"
  const urlPath = `${actions[proposal.value]}-${visaPath}`
  return `/api/v1/declarations/${declaration.value?.id}/${urlPath}/`
})

const requestPayload = computed(() => ({ comment: comment.value, reasons: reasons.value, expiration: delayDays.value }))
const { response, isFetching, execute } = useFetch(url, { headers: headers() }, { immediate: false })
  .post(requestPayload)
  .json()

const submitDecision = async () => {
  v$.value.$reset()
  v$.value.$validate()
  if (v$.value.$error) return

  await execute()
  $externalResults.value = await handleError(response)

  if (response.value.ok) {
    useToaster().addSuccessMessage("Votre décision a été prise en compte")
    clearLocalStorage()
    router.push({ name: "InstructionDeclarations" })
  }
}
</script>

<style scoped>
@reference "../../../styles/index.css";

div.decision-action :deep(.fr-input-group) {
  @apply mb-0;
}

div.changes-needed-fields :deep(.fr-input-group) {
  @apply mb-0;
  @apply mt-1;
}

.fr-multiselect__collapse :deep(.fr-input-group) {
  @apply my-4;
}
</style>
