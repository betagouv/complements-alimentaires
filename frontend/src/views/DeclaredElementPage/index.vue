<template>
  <div>
    <DsfrNotice title="En construction" desc="Des nouvelles fonctionnalités arrivent bientôt !" />
    <div class="fr-container">
      <DsfrBreadcrumb class="mb-8" :links="breadcrumbLinks" />
      <ElementAlert :element="element" />
      <div v-if="element">
        <div class="grid md:grid-cols-2 gap-4">
          <ElementInfo :element="element" :type="type" :declarationLink="declarationLink" />
          <ReplacementSearch @replacement="(obj) => (replacement = obj)" :reset="clearSearch" />
        </div>
        <div class="mt-4">
          <DsfrButtonGroup :buttons="actionButtons" inlineLayoutWhen="md" align="center" class="mb-8" />

          <DsfrModal :opened="!!modalToOpen" :title="modalTitle" :actions="modalActions" @close="closeModal">
            <template #default>
              <div v-if="modalToOpen === 'replace'">
                <p v-if="cannotReplace">
                  Ce n'est pas possible pour l'instant de remplacer une demande avec un ingrédient d'un type different.
                  Veuillez contacter l'équipe Compl'Alim pour effectuer la substitution.
                </p>
                <div v-else>
                  <ElementSynonyms
                    v-model="synonyms"
                    :requestElement="element"
                    :initialSynonyms="replacement.synonyms"
                  />
                </div>
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
import { useRouter } from "vue-router"
import { getApiType } from "@/utils/mappings"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"
import { getNewElementName } from "@/utils/elements"
import ElementInfo from "./ElementInfo"
import ElementAlert from "./ElementAlert"
import ReplacementSearch from "./ReplacementSearch"
import ElementSynonyms from "./ElementSynonyms"

const props = defineProps({ type: String, id: String })

const declarationId = computed(() => element.value?.declaration)
const declarationLink = computed(() => {
  if (!declarationId.value) return
  return { name: "InstructionPage", params: { declarationId: declarationId.value } }
})

const breadcrumbLinks = computed(() => {
  const links = [{ to: { name: "DashboardPage" }, text: "Tableau de bord" }]
  if (lastRoute.value.name === "InstructionPage" && declarationLink.value) {
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
const { data: element, response, execute } = useFetch(url, { immediate: false }).get().json()

const getElementFromApi = async () => {
  await execute()
  await handleError(response)
}

getElementFromApi()
watch(element, (newElement) => {
  if (newElement) {
    const name = getNewElementName(newElement)
    document.title = `${name} - Compl'Alim`
  }
})

// Actions
const modalToOpen = ref(false)
const closeModal = () => (modalToOpen.value = false)

const router = useRouter()
const requestTableRoute = { name: "NewElementsPage" }
// merci https://github.com/vuejs/vue-router/issues/997#issuecomment-1536254142
const lastRoute = computed(() => {
  const backUrl = router.options.history.state.back
  return backUrl ? router.resolve({ path: `${backUrl}` }) : requestTableRoute
})
const navigateBack = (response) => {
  const successRoute = lastRoute.value
  successRoute.query = {
    actionedId: response.id,
    actionedType: response.type,
  }
  router.push(successRoute)
}

const notes = ref()

const openModal = (type) => {
  return () => {
    if (!notes.value) notes.value = element.value?.requestPrivateNotes
    modalToOpen.value = type
  }
}

const replacement = ref()
const synonyms = ref()
watch(replacement, () => {
  // initialiser les synonymes pour permettre la MAJ
  synonyms.value = JSON.parse(JSON.stringify(replacement.value.synonyms || []))
})

const cannotReplace = computed(() => replacement.value?.objectType !== element.value.type)

const actionButtons = computed(() => [
  {
    label: "Remplacer",
    primary: true,
    onclick: openModal("replace"),
    disabled: !replacement.value,
  },
  {
    label: "Demander plus d’information",
    tertiary: true,
    onclick: openModal("info"),
  },
  {
    label: "Refuser l’ingrédient",
    tertiary: true,
    "no-outline": true,
    icon: "ri-close-line",
    onclick: openModal("refuse"),
  },
])

const updateElement = async (action, payload) => {
  const { data, response } = await useFetch(`${url.value}/${action}`, {
    headers: headers(),
  })
    .post(payload)
    .json()
  handleError(response)
  if (data.value) {
    element.value = data.value
  }
  return data.value
}

const modals = computed(() => {
  return {
    replace: {
      title: "Remplace l'ingrédient",
      actions: [
        {
          label: "Remplacer",
          onClick() {
            const payload = {
              element: { id: replacement.value?.id, type: replacement.value?.objectType },
              synonyms: synonyms.value,
            }
            updateElement("replace", payload).then((response) => {
              closeModal()
              navigateBack(response)
            })
          },
          disabled: cannotReplace.value,
        },
      ],
    },
    info: {
      title: "L’ajout du nouvel ingrédient nécessite plus d’information.",
      actions: [
        {
          label: "Enregistrer",
          onClick() {
            updateElement("request-info", {
              requestPrivateNotes: notes.value || "",
            }).then((response) => {
              closeModal()
              navigateBack(response)
            })
          },
        },
      ],
    },
    refuse: {
      title: "L’ajout du nouvel ingrédient sera refusé.",
      actions: [
        {
          label: "Refuser",
          onClick() {
            updateElement("reject", {
              requestPrivateNotes: notes.value || "",
            }).then((response) => {
              closeModal()
              navigateBack(response)
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
</script>
