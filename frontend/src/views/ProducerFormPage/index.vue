<template>
  <div class="fr-container">
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
      <DsfrAlert
        v-if="readonly && payload"
        class="mb-4"
        :type="payload.status === 'AUTHORIZED' ? 'success' : 'info'"
        :title="`Cette déclaration est en statut « ${statusProps[payload.status].label} »`"
      />
      <DsfrTabs
        v-else
        ref="tabs"
        :tab-titles="tabTitles"
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
            ></component>
          </FormWrapper>
        </DsfrTabContent>
      </DsfrTabs>
    </div>
  </div>
</template>
<script setup>
import ProgressSpinner from "@/components/ProgressSpinner"
import { useRootStore } from "@/stores/root"
import { ref, computed, watch } from "vue"
import ProductTab from "./ProductTab"
import CompositionTab from "./CompositionTab"
import SummaryTab from "./SummaryTab"
import AttachmentTab from "./AttachmentTab"
import NewElementTab from "./NewElementTab"
import HistoryTab from "@/components/HistoryTab"
import { useFetch } from "@vueuse/core"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import FormWrapper from "@/components/FormWrapper"
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"
import { statusProps } from "@/utils/mappings"

const $externalResults = ref({})
const route = useRoute()
const router = useRouter()

const selectedTabIndex = ref(parseInt(route.query.tab))
const asc = ref(true)
const tabs = ref(null) // Corresponds to the template ref (https://vuejs.org/guide/essentials/template-refs.html#accessing-the-refs)
const selectTab = async (index) => {
  if (index === selectedTabIndex.value) return
  const saveSuccess = await savePayload()
  if (saveSuccess) {
    asc.value = selectedTabIndex.value < index
    selectedTabIndex.value = index
  }
  tabs.value?.selectIndex?.(selectedTabIndex.value)
}

const store = useRootStore()
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

const components = computed(() => {
  if (readonly.value) return [HistoryTab, SummaryTab]
  const baseComponents = [ProductTab, CompositionTab, AttachmentTab, SummaryTab]
  if (hasNewElements.value) baseComponents.splice(2, 0, NewElementTab)
  if (showHistory.value) baseComponents.splice(0, 0, HistoryTab)
  return baseComponents
})

const tabTitles = computed(() => {
  const idx = (x) => components.value.findIndex((y) => y.__name === x)
  const titleMap = {
    HistoryTab: {
      title: "Historique",
      icon: "ri-chat-3-line",
      tabId: `tab-${idx("HistoryTab")}`,
      panelId: `tab-content-${idx("HistoryTab")}`,
    },
    SummaryTab: {
      title: "Soumettre",
      icon: "ri-mail-send-line",
      tabId: `tab-${idx("SummaryTab")}`,
      panelId: `tab-content-${idx("SummaryTab")}`,
    },
    ProductTab: {
      title: "Le produit",
      icon: "ri-capsule-fill",
      tabId: `tab-${idx("ProductTab")}`,
      panelId: `tab-content-${idx("ProductTab")}`,
    },
    CompositionTab: {
      title: "Composition",
      icon: "ri-test-tube-line",
      tabId: `tab-${idx("CompositionTab")}`,
      panelId: `tab-content-${idx("CompositionTab")}`,
    },
    AttachmentTab: {
      title: "Pièces jointes",
      icon: "ri-file-text-line",
      tabId: `tab-${idx("AttachmentTab")}`,
      panelId: `tab-content-${idx("AttachmentTab")}`,
    },
    NewElementTab: {
      title: "Nouveaux éléments",
      icon: "ri-flask-line",
      tabId: `tab-${idx("NewElementTab")}`,
      panelId: `tab-content-${idx("NewElementTab")}`,
    },
  }
  return components.value.map((x) => titleMap[x.__name])
})

const savePayload = async () => {
  const isNewDeclaration = !payload.value.id
  const url = isNewDeclaration
    ? `/api/v1/users/${store.loggedUser.id}/declarations/`
    : `/api/v1/declarations/${payload.value.id}`
  const httpMethod = isNewDeclaration ? "post" : "put"
  const { response, data } = await useFetch(url, { headers: headers() })[httpMethod](payload).json()
  $externalResults.value = await handleError(response)
  if ($externalResults.value) {
    useToaster().addErrorMessage("Merci de vérifier les champs en rouge pour pouvoir changer d'onglet")
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
  const path = payload.value.status === "DRAFT" ? "submit" : "resubmit"
  const url = `/api/v1/declarations/${payload.value.id}/${path}/`
  const { response } = await useFetch(url, { headers: headers() }).post({ comment }).json()
  $externalResults.value = await handleError(response)

  if ($externalResults.value) {
    // Temporairement, on montrera les messages des champs en haut du formulaire car
    // ils peuvent être présents dans plusierus steps. Cette UI/UX pourra être amélioré
    // par la suite.
    const fieldErrors = $externalResults.value.fieldErrors.map((x) => Object.values(x)?.[0])
    $externalResults.value.nonFieldErrors.push(...fieldErrors)
    //
    window.scrollTo(0, 0)
  } else {
    useToaster().addSuccessMessage("Votre déclaration a été envoyée")
    router.replace({ name: "DeclarationsHomePage" })
  }
}

watch(
  () => route.query.tab,
  (tab) => selectTab(parseInt(tab))
)
</script>
