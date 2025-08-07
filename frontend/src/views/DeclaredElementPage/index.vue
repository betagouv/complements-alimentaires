<template>
  <div>
    <div class="fr-container">
      <DsfrBreadcrumb class="mb-8" :links="breadcrumbLinks" />
      <ElementAlert :element="element" />
      <div v-if="element">
        <div class="grid md:grid-cols-2 gap-4">
          <ElementInfo :element="element" :type="type" :declarationLink="declarationLink" />
          <ReplacementSearch @replacement="(obj) => (replacement = obj)" v-if="!element.isPartRequest" />
        </div>
        <div v-if="replacement" class="my-4">
          <ElementCard :objectType="replacement.objectType" v-model="additionalFields" :canRemove="false" />
        </div>
        <div class="mt-4">
          <DsfrButtonGroup :buttons="actionButtons" inlineLayoutWhen="md" align="center" class="mb-8" />

          <DsfrModal :opened="!!modalToOpen" :title="modalTitle" :actions="modalActions" @close="closeModal">
            <template #default>
              <div v-if="modalToOpen === 'replace'">
                <ElementSynonyms v-model="synonyms" :requestElement="element" :initialSynonyms="replacement.synonyms" />
              </div>
              <div v-else-if="modalToOpen === 'authorizePart'">
                <p>
                  Voulez-vous autoriser la partie de plante {{ plantPartName }} pour la plante
                  {{ element.element?.name }} ?
                </p>
              </div>
              <div v-else>
                <DsfrInput v-model="notes" label="Notes" label-visible is-textarea />
              </div>
            </template>
          </DsfrModal>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch, ref } from "vue"
import { useFetch } from "@vueuse/core"
import { useRootStore } from "@/stores/root"
import { useRouter } from "vue-router"
import { getApiType } from "@/utils/mappings"
import { headers } from "@/utils/data-fetching"
import { getActivityReadonlyByType } from "@/utils/mappings"
import useToaster from "@/composables/use-toaster"
import ElementInfo from "./ElementInfo"
import ElementAlert from "./ElementAlert"
import ReplacementSearch from "./ReplacementSearch"
import ElementCard from "@/components/ElementCard"
import ElementSynonyms from "./ElementSynonyms"
import { setDocumentTitle } from "@/utils/document"

const props = defineProps({ type: String, id: String })
const store = useRootStore()
const { addErrorMessage } = useToaster()

const declarationId = computed(() => element.value?.declaration)
const declarationLink = computed(() => {
  if (!declarationId.value) return
  return { name: "InstructionPage", params: { declarationId: declarationId.value } }
})

const lastRoute = computed(() => router.getPreviousRoute().value)
const breadcrumbLinks = computed(() => {
  const links = [{ to: { name: "DashboardPage" }, text: "Tableau de bord" }]
  if (lastRoute.value?.name === "InstructionPage" && declarationLink.value) {
    links.push({ to: { name: "InstructionDeclarations" }, text: "Déclarations pour instruction" })
    links.push({ to: lastRoute.value, text: "Instruction" })
  } else {
    links.push({ to: requestTableRoute, text: "Tableau de demandes" })
  }
  links.push({ text: "Demande d'ajout d'ingrédient" })
  return links
})

// Init
const url = computed(() => `/api/v1/declared-elements/${getApiType(props.type)}/${props.id}`)
const onFetchError = ({ error, data }) => {
  addErrorMessage("Une erreur est survenu. Merci de réessayer ultérieurement.")
  return { error, data }
}
const { data: element, execute } = useFetch(url, { immediate: false, onFetchError }).get().json()

const getElementFromApi = async () => {
  await execute()
}

getElementFromApi()
watch(element, (newElement) => {
  setDocumentTitle([newElement?.newName || newElement?.element?.name, "Nouvel ingrédient"])
  additionalFields.value = JSON.parse(JSON.stringify(element.value))
  additionalFields.value.new = false
})

// Actions
const modalToOpen = ref(false)
const closeModal = () => (modalToOpen.value = false)

const router = useRouter()
const requestTableRoute = { name: "NewElementsPage" }

const notes = ref()

const openModal = (type) => {
  return () => {
    if (!notes.value) notes.value = element.value?.requestPrivateNotes
    modalToOpen.value = type
  }
}

const replacement = ref()

const additionalFields = ref({})
store.fetchDeclarationFieldsData()

const synonyms = ref()

watch(replacement, (newReplacement) => {
  // initialiser les synonymes pour permettre la MAJ
  synonyms.value = JSON.parse(JSON.stringify(newReplacement.synonyms || []))
  additionalFields.value.element = JSON.parse(JSON.stringify(newReplacement))
  // le suivant devrait copier la logique pertinate de addElement, définit dans CompositionTab
  if (getActivityReadonlyByType(newReplacement.objectType)) {
    // si l'activité n'est pas modifiable pour le nouveau type, s'assurer qu'on suit la même logique que CompositionTab, addElement
    // sinon, utilise l'activité définit par le pro avec la demande
    additionalFields.value.active = !!newReplacement.activity
  }
  if (newReplacement.objectType === "microorganism" && newReplacement.objectType !== element.value.objectType) {
    additionalFields.value.activated = true
  }
})

const actionButtons = computed(() => {
  const actions = [
    {
      label: "Demander plus d’information",
      tertiary: true,
      onclick: openModal("info"),
      disabled: element.value.isPartRequest && element.value.requestStatus === "REPLACED",
    },
    {
      label: element.value.isPartRequest ? "Refuser la partie de plante" : "Refuser l’ingrédient",
      tertiary: true,
      "no-outline": true,
      icon: "ri-close-line",
      onclick: openModal("refuse"),
      disabled: element.value.isPartRequest && element.value.requestStatus === "REPLACED",
    },
  ]
  if (element.value.isPartRequest) {
    actions.unshift({
      label: "Autoriser la partie de plante",
      primary: true,
      onclick: openModal("authorizePart"),
      disabled: element.value.isPartRequest && element.value.requestStatus === "REPLACED",
    })
  } else {
    actions.unshift({
      label: "Remplacer",
      primary: true,
      onclick: openModal("replace"),
      disabled: !replacement.value,
    })
  }
  return actions
})

const updateElement = async (action, payload) => {
  const { data, response } = await useFetch(`${url.value}/${action}`, { headers: headers() }, { onFetchError })
    .post(payload)
    .json()

  if (response.value?.ok) {
    closeModal()
    router.navigateBack(requestTableRoute, { query: { actionedId: data.value.id, actionedType: data.value.type } })
  }
}

const modals = computed(() => {
  return {
    replace: {
      title: "Remplace l'ingrédient",
      actions: [
        {
          label: "Remplacer",
          onClick() {
            const info = JSON.parse(JSON.stringify(additionalFields.value))
            delete info.element
            const payload = {
              element: { id: replacement.value?.id, type: getApiType(replacement.value?.objectType) },
              synonyms: synonyms.value,
              additionalFields: info,
            }
            updateElement("replace", payload)
          },
        },
      ],
    },
    authorizePart: {
      title: "Autoriser la partie de plante",
      actions: [
        {
          label: "Autoriser la partie de plante",
          onClick() {
            updateElement("accept-part", {})
          },
        },
      ],
    },
    info: {
      title: element.value.isPartRequest
        ? "L'autorisation de la partie de plante nécessite plus d'information"
        : "L’ajout du nouvel ingrédient nécessite plus d’information.",
      actions: [
        {
          label: "Enregistrer",
          onClick() {
            updateElement("request-info", {
              requestPrivateNotes: notes.value || "",
            })
          },
        },
      ],
    },
    refuse: {
      title: element.value.isPartRequest
        ? "L'autorisation de la partie de plante sera refusé"
        : "L’ajout du nouvel ingrédient sera refusé.",
      actions: [
        {
          label: "Refuser",
          onClick() {
            updateElement("reject", {
              requestPrivateNotes: notes.value || "",
            })
          },
        },
      ],
    },
  }
})
const modalTitle = computed(() => modals.value[modalToOpen.value]?.title)

const modalActions = computed(() => {
  const actions = modals.value[modalToOpen.value]?.actions || []
  return actions.concat([
    {
      label: "Annuler",
      secondary: true,
      onClick() {
        closeModal()
      },
    },
  ])
})

const plantPartName = computed(() => {
  return store.plantParts?.find((p) => p.id === element.value.usedPart)?.name
})
</script>
