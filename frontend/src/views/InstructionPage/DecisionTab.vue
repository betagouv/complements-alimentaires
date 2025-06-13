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
            class="col-span-2 sm:col-span-1 mb-0!"
          >
            <template v-slot:label>
              <div class="font-bold">
                <v-icon :color="category.color" :name="category.icon" aria-hidden />
                {{ category.title }}
              </div>
              <p class="fr-text--sm mb-0!">
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
        <div class="mb-8" v-for="reason in blockingReasons" :key="reason.title">
          <p class="font-bold">{{ reason.title }}</p>
          <DsfrCheckboxSet
            v-model="reasons"
            :options="reason.items.map((x) => ({ label: x, value: x }))"
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
          <DsfrButton
            label="Soumettre"
            @click="submitDecision"
            :disabled="isFetching || (needsAnsesReferal && decisionCategory === 'approve')"
          />
          <div v-if="needsAnsesReferal && decisionCategory === 'approve'" class="mt-2">
            <hr class="p-0 my-2" />
            <p class="my-1">
              <v-icon name="ri-error-warning-line"></v-icon>
              La déclaration ne peut pas être validée en nécessitant une saisine ANSES. Merci de changer l'article avant
              de la valider.
            </p>
            <ArticleInfoRow v-model="declaration" v-if="needsAnsesReferal && decisionCategory === 'approve'" />
          </div>

          <div v-if="firstErrorMsg(v$, 'reasons')">{{ firstErrorMsg(v$, "reasons") }}</div>
        </template>
      </DsfrHighlight>
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
import { blockingReasons, decisionCategories } from "@/utils/mappings"

const decisionCategory = ref(null)
watch(decisionCategory, () => (proposal.value = decisionCategory.value === "approve" ? "autorisation" : null))

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
const proposal = ref(null)
const delayDays = ref()
const comment = ref(declaration.value?.lastAdministrationComment || "")
const reasons = ref([])

const $externalResults = ref({})
const v$ = useVuelidate(rules, { comment, proposal, reasons, delayDays }, { $externalResults })

const emit = defineEmits(["decision-done"])

const needsVisa = ref(false)
const mandatoryVisaProposals = ["objection", "rejection"]
const disableVisaCheckbox = computed(() => !proposal.value || mandatoryVisaProposals.indexOf(proposal.value) > -1)
const disableDelayDays = computed(() => proposal.value === "rejection")
watch(proposal, (newProposal) => {
  if (mandatoryVisaProposals.indexOf(newProposal) > -1) needsVisa.value = true
  else needsVisa.value = false
  if (newProposal === "objection") delayDays.value = 30
  else if (newProposal === "observation") delayDays.value = 15
  else delayDays.value = null
})

const needsAnsesReferal = computed(() => declaration.value?.article === "ANSES_REFERAL")

const proposalOptions = computed(() => {
  if (decisionCategory.value === "approve") return [{ text: "Autorisation", value: "autorisation" }]

  return [
    { text: "Observation", value: "observation" },
    { text: "Objection", value: "objection" },
    { text: "Refus", value: "rejection" },
  ]
})

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
    emit("decision-done")
  }
}
</script>

<style scoped>
@reference "../../styles/index.css";

.reject-reasons:deep(.fr-input-group) {
  @apply mb-0!;
}
.visa-checkbox:deep(.fr-fieldset__element) {
  @apply mb-1!;
}
</style>
