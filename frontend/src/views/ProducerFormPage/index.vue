<template>
  <div class="fr-container overflow-hidden">
    <DsfrBreadcrumb
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { to: { name: 'DeclarationsHomePage' }, text: 'Mes déclarations' },
        { text: isNewDeclaration ? 'Nouvelle déclaration' : 'Détails de ma déclaration' },
      ]"
    />

    <div v-if="isFetching" class="flex justify-center items-center min-h-60">
      <ProgressSpinner />
    </div>

    <div v-else class="mb-4">
      <DeclarationAlert v-if="payload" role="declarant" :declaration="payload" :snapshots="snapshots" class="mb-4" />

      <DsfrAlert
        class="mb-4"
        v-if="payload.id && !payload.author && !payload.siccrfId"
        type="info"
        title="Cette déclaration n'est gérée par personne"
      >
        <p>Vous pouvez néanmoins vous l'assigner en cliquant ci-dessous</p>
        <DsfrButton class="mt-2" label="Prendre cette déclaration" tertiary @click="takeDeclaration" />
      </DsfrAlert>
      <DsfrAlert
        class="mb-4"
        v-else-if="payload.author && payload.author !== loggedUser.id && !payload.siccrfId"
        type="info"
        title="Cette déclaration est gérée par une autre personne"
      >
        <p>Vous pouvez néanmoins vous l'assigner en cliquant ci-dessous</p>
        <DsfrButton class="mt-2" label="Prendre cette déclaration" tertiary @click="takeDeclaration" />
      </DsfrAlert>

      <StatusChangeErrorDisplay class="mb-8" :errors="statusChangeErrors" :tabTitles="titles" />
      <DsfrTabs
        v-if="payload"
        ref="tabs"
        :tab-titles="titles"
        v-model="selectedTabIndex"
        @update:modelValue="selectTab"
        class="allow-overflow"
      >
        <div class="absolute opacity-50 bg-slate-200 inset-0 z-10 flex justify-center pt-20" v-if="requestInProgress">
          <ProgressSpinner />
        </div>
        <DsfrTabContent
          v-for="(component, idx) in components"
          :key="`component-${idx}`"
          :panelId="`tab-content-${idx}`"
          :tabId="`tab-${idx}`"
        >
          <FormWrapper :externalResults="$externalResults">
            <component
              :is="component"
              v-model="payload"
              @submit="submitPayload"
              :externalResults="$externalResults"
              :readonly="readonly"
              :declarationId="id"
              :snapshots="snapshots"
              @withdraw="onWithdrawal"
              :hideInstructionDetails="true"
            ></component>
          </FormWrapper>
        </DsfrTabContent>
      </DsfrTabs>
      <TabStepper
        v-if="payload"
        :titles="titles"
        :selectedTabIndex="selectedTabIndex"
        @back="selectTab(selectedTabIndex - 1)"
        @forward="selectTab(selectedTabIndex + 1)"
        :removeSaveLabel="readonly"
      />
      <hr class="mt-6" />
      <DeletionModal
        @delete="deleteDeclaration"
        v-if="showDeletionModal"
        class="mb-4"
        :buttonLabel="isDraft ? 'Supprimer mon brouillon' : 'Abandonner cette déclaration'"
        :helperText="isDraft ? 'Votre déclaration est en brouillon' : ''"
        :actionButtonLabel="isDraft ? 'Supprimer mon brouillon' : 'Abandonner cette déclaration'"
        :modalText="
          isDraft
            ? 'La suppression de votre déclaration n\'est pas réversible. Êtes-vous sûr de vouloir procéder ?'
            : 'En mettant votre déclaration en abandon le procesus d\'instruction sera interrompu. Êtes-vous sûr de vouloir continuer ?'
        "
        :productName="payload.name"
      />
    </div>
  </div>
</template>
<script setup>
import DeclarationAlert from "@/components/DeclarationAlert"
import ProgressSpinner from "@/components/ProgressSpinner"
import StatusChangeErrorDisplay from "./StatusChangeErrorDisplay"
import TabStepper from "@/components/TabStepper"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { ref, computed, watch, onMounted } from "vue"
import ProductTab from "./ProductTab"
import CompositionTab from "./CompositionTab"
import SummaryTab from "./SummaryTab"
import AttachmentTab from "./AttachmentTab"
import NewElementTab from "./NewElementTab"
import DeletionModal from "./DeletionModal"
import HistoryTab from "@/components/HistoryTab"
import WithdrawalTab from "@/components/WithdrawalTab"
import { useFetch } from "@vueuse/core"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import FormWrapper from "@/components/FormWrapper"
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"
import { tabTitles } from "@/utils/mappings"
import { setDocumentTitle } from "@/utils/document"
import { hasNewElements } from "@/utils/elements"

// Il y a deux refs qui stockent des erreurs. $externalResults sert
// lors qu'on sauvegarde la déclaration (POST ou PUT) mais qu'on ne change
// pas son status. Des erreurs ici empêchent de changer l'onglet. Exemple : lors
// qu'on ne me pas de nom du produit on ne peut pas avancer.
const $externalResults = ref({})

// Les erreurs suite à une tentative de changement de statut sont stockés dans
// ce ref. C'est toujours possible de changer d'onglet pour corriger les erreurs.
// Exemple : le manque d'une pièce jointe pour l'étiquetage.
const statusChangeErrors = ref({})

const route = useRoute()
const router = useRouter()

const previouslySelectedTabIndex = ref(parseInt(route.query.tab))
const selectedTabIndex = ref(parseInt(route.query.tab))

const selectTab = async (index) => {
  if (requestInProgress.value) return

  // Si va vers le `SummaryTab` on calcule l'article. Ceci est un workaround pour éviter
  // de calculer l'article dans le backend à chaque modification (ça peut être cher en termes
  // de performance).
  const forceArticleCalculation = !readonly.value && components.value[index] === SummaryTab
  const allowTransition = readonly.value || (await savePayload({ forceArticleCalculation }))
  if (allowTransition) {
    router.replace({ query: { tab: index } })
    previouslySelectedTabIndex.value = index
  } else {
    selectedTabIndex.value = previouslySelectedTabIndex.value
  }
}

const requestInProgress = ref(false)

const store = useRootStore()
const { loggedUser } = storeToRefs(store)
store.fetchDeclarationFieldsData()

const props = defineProps({
  id: String,
})
const isNewDeclaration = computed(() => !props.id)

const payload = ref({
  effects: [],
  conditionsNotRecommended: [],
  populations: [],
  elements: [],
  declaredPlants: [],
  declaredMicroorganisms: [],
  declaredIngredients: [],
  declaredSubstances: [],
  computedSubstances: [],
  attachments: [],
})
const { response, data, isFetching, execute } = useFetch(`/api/v1/declarations/${props.id || route.query.duplicate}`, {
  immediate: false,
})
  .get()
  .json()

const {
  response: snapshotsResponse,
  data: snapshots,
  execute: executeSnapshotsFetch,
} = useFetch(() => `/api/v1/declarations/${props.id}/snapshots/`, { immediate: false })
  .get()
  .json()

if (!isNewDeclaration.value || route.query.duplicate) execute()
if (!isNewDeclaration.value && !route.query.duplicate) executeSnapshotsFetch()

watch(response, () => handleError(response))
watch(snapshotsResponse, () => handleError(snapshotsResponse))
watch(data, () => {
  const shouldDuplicate = route.query.duplicate && !props.id
  if (shouldDuplicate) {
    performDuplication(data.value)
    const successMessage = "Votre déclaration a été dupliquée. Merci de renseigner les pièces jointes."
    savePayload({ successMessage })
  } else payload.value = data.value
  setDocumentTitleForTab(selectedTabIndex.value, data)
})

const readonly = computed(
  () =>
    !isNewDeclaration.value &&
    payload.value.status !== "DRAFT" &&
    payload.value.status !== "OBSERVATION" &&
    payload.value.status !== "OBJECTION"
)

const showHistory = computed(
  () => !payload.value.siccrfId && (readonly.value || (!isNewDeclaration.value && !isDraft.value))
)
const showWithdrawal = computed(() => payload.value.status === "AUTHORIZED")

const components = computed(() => {
  const baseComponents = readonly.value ? [SummaryTab] : [ProductTab, CompositionTab, AttachmentTab, SummaryTab]

  if (!readonly.value && hasNewElements(payload.value)) baseComponents.splice(2, 0, NewElementTab)
  if (showHistory.value) baseComponents.splice(0, 0, HistoryTab)
  if (showWithdrawal.value) baseComponents.push(WithdrawalTab)
  return baseComponents
})

const titles = computed(() => tabTitles(components.value, !readonly.value))

const savePayload = async ({
  successMessage = "Votre démarche a été sauvegardée",
  forceArticleCalculation = false,
} = {}) => {
  const isNewDeclaration = !payload.value.id
  const url = isNewDeclaration
    ? `/api/v1/users/${loggedUser.value.id}/declarations/${forceArticleCalculation ? "?force-article-calculation=true" : ""}`
    : `/api/v1/declarations/${payload.value.id}${forceArticleCalculation ? "?force-article-calculation=true" : ""}`
  const httpMethod = isNewDeclaration ? "post" : "put"
  requestInProgress.value = true
  const { response, data } = await useFetch(url, { headers: headers() })[httpMethod](payload).json()
  requestInProgress.value = false
  $externalResults.value = await handleError(response)
  const hasError = !!$externalResults.value
  if (hasError) {
    const fieldErrors = $externalResults.value.fieldErrors
    if (fieldErrors && Object.keys(fieldErrors).length > 0) {
      useToaster().addErrorMessage(
        "Merci de vérifier que les champs obligatoires, signalés par une astérix *, ont bien été remplis pour pouvoir changer d'onglet"
      )
      window.scrollTo(0, 0)
    }
    return false
  } else {
    payload.value = data.value
    // Une fois sauvegardé on change l'URL pour indiquer qu'on est en train de modifier une déclaration
    // existante. Ça permet aussi de faire un refresh ou back sans problème.
    if (route.name === "NewDeclaration") {
      await router.replace({
        name: "DeclarationPage",
        params: { id: data.value.id },
        query: route.query,
      })
    }
    // L'ID permet de ne pas montrer plusieurs messages de succès lors qu'on passe par
    // les étapes un peu rapidement
    useToaster().addMessage({
      type: "success",
      id: "declaration-success",
      description: successMessage,
    })
    return true
  }
}

const isDraft = computed(() => payload.value?.status === "DRAFT")

const submitPayload = async (comment) => {
  if (requestInProgress.value) return
  const path = isDraft.value ? "submit" : "resubmit"
  const url = `/api/v1/declarations/${payload.value.id}/${path}/`

  requestInProgress.value = true
  const { response } = await useFetch(url, { headers: headers() }).post({ comment }).json()
  requestInProgress.value = false

  statusChangeErrors.value = await handleError(response)

  if (statusChangeErrors.value) {
    window.scrollTo(0, 0)
  } else {
    useToaster().addSuccessMessage("Votre déclaration a été envoyée")
    router.replace({ name: "DeclarationsHomePage" })
  }
}

const showDeletionModal = computed(() => {
  const statuses = [
    "DRAFT",
    "AWAITING_INSTRUCTION",
    "ONGOING_INSTRUCTION",
    "AWAITING_VISA",
    "ONGOING_VISA",
    "OBJECTION",
    "OBSERVATION",
  ]
  return statuses.indexOf(payload.value?.status) > -1
})

const deleteDeclaration = async () => {
  if (requestInProgress.value) return
  const url = isDraft.value
    ? `/api/v1/declarations/${payload.value.id}`
    : `/api/v1/declarations/${payload.value.id}/abandon/`

  const requestFunction = isDraft.value
    ? useFetch(url, { headers: headers() }).delete
    : useFetch(url, { headers: headers() }).post

  requestInProgress.value = true
  const { response } = await requestFunction().json()
  requestInProgress.value = false

  statusChangeErrors.value = await handleError(response)
  if (statusChangeErrors.value) {
    window.scrollTo(0, 0)
  } else {
    const message = isDraft.value ? "Votre brouillon a été supprimée" : "Votre déclaration a été mise en abandon"
    useToaster().addSuccessMessage(message)
    router.replace({ name: "DeclarationsHomePage" })
  }
}

const takeDeclaration = async () => {
  const url = `/api/v1/declarations/${payload.value.id}/take-authorship/`
  await useFetch(url, { headers: headers() }).post()
  execute()
}

const onWithdrawal = () => router.replace({ name: "DeclarationsHomePage", query: { status: "WITHDRAWN,AUTHORIZED" } })

const setDocumentTitleForTab = (tabIdx, fromData) => {
  let declarationTitle = isNewDeclaration.value ? "Nouvelle démarche" : `Déclaration « ${fromData.value.name} »`
  if (readonly.value) declarationTitle = `Détails de ma déclaration « ${fromData.value.name} »`
  setDocumentTitle(
    [titles.value[tabIdx]?.title, declarationTitle],
    readonly.value
      ? undefined
      : {
          number: tabIdx + 1,
          total: titles.value.length,
          term: "étape",
        }
  )
}

watch(
  () => route.query.tab,
  (tab) => {
    selectedTabIndex.value = parseInt(tab)
    setDocumentTitleForTab(selectedTabIndex.value, payload)
  }
)

onMounted(() => setDocumentTitleForTab(selectedTabIndex.value, payload))

const performDuplication = (originalDeclaration) => {
  // Prendre uniquement les champs pertinents. C'est préférable d'utiliser une
  // whitelist pour s'assurer qu'un champ non souhaité ne se faufile pas dans la
  // duplication
  const fieldsToKeep = [
    "company",
    "address",
    "additionalDetails",
    "postalCode",
    "city",
    "cedex",
    "country",
    "name",
    "brand",
    "gamme",
    "flavor",
    "description",
    "galenicFormulation",
    "unitQuantity",
    "unitMeasurement",
    "conditioning",
    "dailyRecommendedDose",
    "minimumDuration",
    "instructions",
    "warning",
    "populations",
    "conditionsNotRecommended",
    "effects",
    "declaredPlants",
    "declaredMicroorganisms",
    "declaredIngredients",
    "declaredSubstances",
    "computedSubstances",
    "otherEffects",
    "otherGalenicFormulation",
    "otherConditions",
  ]

  fieldsToKeep.forEach((x) => (payload.value[x] = originalDeclaration[x]))

  // Enlever les IDs des éléments de la composition
  payload.value.declaredPlants.forEach((x) => delete x.id)
  payload.value.declaredMicroorganisms.forEach((x) => delete x.id)
  payload.value.declaredSubstances.forEach((x) => delete x.id)
  payload.value.declaredIngredients.forEach((x) => delete x.id)
  payload.value.computedSubstances.forEach((x) => delete x.id)
}
</script>

<style scoped>
.allow-overflow {
  overflow: visible;
  position: relative;
}
</style>
