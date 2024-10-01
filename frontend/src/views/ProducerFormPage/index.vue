<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { to: { name: 'DeclarationsHomePage' }, text: 'Mes déclarations' },
        { text: isNewDeclaration ? 'Nouvelle déclaration' : 'Détails de ma déclaration' },
      ]"
    />

    <DeletionModal @delete="deleteDeclaration" v-if="payload.status === 'DRAFT' && payload.author === loggedUser.id" />

    <div v-if="isFetching" class="flex justify-center items-center min-h-60">
      <ProgressSpinner />
    </div>

    <div v-else class="mb-4">
      <DeclarationAlert v-if="payload" role="declarant" :declaration="payload" class="mb-4" />

      <DsfrAlert
        class="mb-4"
        v-if="payload.author !== loggedUser.id"
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
        :initialSelectedIndex="parseInt(route.query.tab)"
        @select-tab="(tab) => router.replace({ query: { tab } })"
      >
        <DsfrTabContent
          v-for="(component, idx) in components"
          :key="`component-${idx}`"
          :panelId="`tab-content-${idx}`"
          :tabId="`tab-${idx}`"
          :selected="selectedTabIndex === idx"
          :asc="asc"
        >
          <FormWrapper :externalResults="$externalResults">
            <component
              :is="component"
              v-model="payload"
              @submit="submitPayload"
              :externalResults="$externalResults"
              :readonly="readonly"
              :declarationId="id"
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
import { ref, computed, watch } from "vue"
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

const selectedTabIndex = ref(parseInt(route.query.tab))
const asc = ref(true)
const tabs = ref(null) // Corresponds to the template ref (https://vuejs.org/guide/essentials/template-refs.html#accessing-the-refs)
const selectTab = async (index) => {
  if (requestInProgress.value || index === selectedTabIndex.value) return
  const allowTransition = readonly.value || (await savePayload())
  if (allowTransition) {
    asc.value = selectedTabIndex.value < index
    selectedTabIndex.value = index
  }
  tabs.value?.selectIndex?.(selectedTabIndex.value)
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
const { response, data, isFetching, execute } = useFetch(`/api/v1/declarations/${props.id}`, { immediate: false })
  .get()
  .json()

if (!isNewDeclaration.value) execute()

watch(response, () => handleError(response))
watch(data, () => (payload.value = data.value))

const hasNewElements = computed(() => {
  return []
    .concat(
      payload.value.declaredPlants,
      payload.value.declaredMicroorganisms,
      payload.value.declaredIngredients,
      payload.value.declaredSubstances
    )
    .some((x) => x.new)
})
const readonly = computed(
  () =>
    !isNewDeclaration.value &&
    payload.value.status !== "DRAFT" &&
    payload.value.status !== "OBSERVATION" &&
    payload.value.status !== "OBJECTION"
)

const showHistory = computed(() => readonly.value || (!isNewDeclaration.value && payload.value.status !== "DRAFT"))
const showWithdrawal = computed(() => payload.value.status === "AUTHORIZED")

const components = computed(() => {
  const baseComponents = readonly.value ? [SummaryTab] : [ProductTab, CompositionTab, AttachmentTab, SummaryTab]

  if (!readonly.value && hasNewElements.value) baseComponents.splice(2, 0, NewElementTab)
  if (showHistory.value) baseComponents.splice(0, 0, HistoryTab)
  if (showWithdrawal.value) baseComponents.push(WithdrawalTab)
  return baseComponents
})

const titles = computed(() => tabTitles(components.value, !readonly.value))

const savePayload = async () => {
  const isNewDeclaration = !payload.value.id
  const url = isNewDeclaration
    ? `/api/v1/users/${loggedUser.value.id}/declarations/`
    : `/api/v1/declarations/${payload.value.id}`
  const httpMethod = isNewDeclaration ? "post" : "put"
  requestInProgress.value = true
  const { response, data } = await useFetch(url, { headers: headers() })[httpMethod](payload).json()
  requestInProgress.value = false
  $externalResults.value = await handleError(response)
  if ($externalResults.value) {
    useToaster().addErrorMessage(
      "Merci de vérifier que les champs obligatoires, signalés par une astérix *, ont bien été remplis pour pouvoir changer d'onglet"
    )
    window.scrollTo(0, 0)
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
      description: "Votre démarche a été sauvegardée",
    })
    return true
  }
}

const submitPayload = async (comment) => {
  if (requestInProgress.value) return
  const path = payload.value.status === "DRAFT" ? "submit" : "resubmit"
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

const deleteDeclaration = async () => {
  if (requestInProgress.value || !payload.value.status === "DRAFT") return
  const url = `/api/v1/declarations/${payload.value.id}`
  requestInProgress.value = true
  const { response } = await useFetch(url, { headers: headers() }).delete().json()
  requestInProgress.value = false

  statusChangeErrors.value = await handleError(response)
  if (statusChangeErrors.value) {
    window.scrollTo(0, 0)
  } else {
    useToaster().addSuccessMessage("Votre déclaration a été supprimée")
    router.replace({ name: "DeclarationsHomePage" })
  }
}

const takeDeclaration = async () => {
  const url = `/api/v1/declarations/${payload.value.id}/take-authorship/`
  await useFetch(url, { headers: headers() }).post()
  execute()
}

const onWithdrawal = () => router.replace({ name: "DeclarationsHomePage", query: { status: "WITHDRAWN,AUTHORIZED" } })

watch(
  () => route.query.tab,
  (tab) => selectTab(parseInt(tab))
)
</script>
