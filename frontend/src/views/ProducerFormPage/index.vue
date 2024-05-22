<template>
  <div class="bg-blue-france-975 border border-slate-300">
    <div class="fr-container pt-4 pb-6" v-if="steps.length > 1">
      <DsfrStepper class="!mb-0" :currentStep="currentStep" :steps="steps" />
    </div>
  </div>

  <div class="fr-container" v-if="!isFetching">
    <StepButtons
      class="mb-6 mt-3"
      @next="goForward"
      @previous="goBackward"
      :disablePrevious="disablePrevious"
      :disableNext="disableNext"
      v-if="steps.length > 1"
    />
    <FormWrapper :externalResults="$externalResults">
      <component
        :is="components[currentStep - 1]"
        v-model="payload"
        @submit="submitPayload"
        :externalResults="$externalResults"
        :readonly="readonly"
      ></component>
    </FormWrapper>
    <StepButtons
      class="mb-3 mt-6"
      @next="goForward"
      @previous="goBackward"
      :disablePrevious="disablePrevious"
      :disableNext="disableNext"
      v-if="steps.length > 1"
    />
  </div>
</template>
<script setup>
import { useRootStore } from "@/stores/root"
import { onMounted, ref, computed, watch } from "vue"
import ProductStep from "./ProductStep"
import CompositionStep from "./CompositionStep"
import SummaryStep from "./SummaryStep"
import AttachmentStep from "./AttachmentStep"
import NewElementStep from "./NewElementStep"
import StepButtons from "./StepButtons"
import { useFetch } from "@vueuse/core"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import FormWrapper from "@/components/FormWrapper"
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"

const $externalResults = ref({})

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
const readonly = computed(() => !isNewDeclaration.value && payload.value.status !== "DRAFT")
const currentStep = ref(null)
const steps = computed(() => {
  if (readonly.value) return ["Résumé"]
  const baseSteps = ["Le produit", "La composition", "Pièces jointes", "Résumé"]
  if (hasNewElements.value) baseSteps.splice(2, 0, "Nouveaux éléments")
  return baseSteps
})

const components = computed(() => {
  if (readonly.value) return [SummaryStep]
  const baseComponents = [ProductStep, CompositionStep, AttachmentStep, SummaryStep]
  if (hasNewElements.value) baseComponents.splice(2, 0, NewElementStep)
  return baseComponents
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
    useToaster().addErrorMessage("Merci de vérifier les champs en rouge")
    window.scrollTo(0, 0)
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
  }
}

const submitPayload = async () => {
  const url = `/api/v1/declarations/${payload.value.id}/submit/`
  const { response } = await useFetch(url, { headers: headers() }).post().json()
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

const goForward = async () => {
  await savePayload()
  if (!$externalResults.value) router.push({ query: { step: currentStep.value + 1 } })
}
const goBackward = async () => {
  await savePayload()
  if (!$externalResults.value) router.push({ query: { step: currentStep.value - 1 } })
}

const disablePrevious = computed(() => currentStep.value === 1)
const disableNext = computed(() => currentStep.value === steps.value.length)

const route = useRoute()
const router = useRouter()

const ensureStepInUrl = () => {
  // Si c'est une nouvelle déclaration, on doit obligatoirement commencer avec le step 1
  if (isNewDeclaration.value) router.replace({ query: { step: 1 } })

  if (route.query.step && parseInt(route.query.step) >= 1 && parseInt(route.query.step) <= steps.value.length)
    currentStep.value = parseInt(route.query.step)
  else router.replace({ query: { step: 1 } })
}

onMounted(ensureStepInUrl)
watch(() => route.query.step, ensureStepInUrl)
</script>
