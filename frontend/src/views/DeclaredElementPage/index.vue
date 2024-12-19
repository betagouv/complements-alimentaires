<template>
  <div>
    <DsfrNotice title="En construction" desc="Des nouvelles fonctionnalités arrivent bientôt !" />
    <div class="fr-container">
      <DsfrBreadcrumb class="mb-8" :links="breadcrumbLinks" />
      <DsfrAlert v-if="alert" v-bind="alert" class="mb-4" />
      <div v-if="element">
        <div class="grid md:grid-cols-2 gap-4">
          <ElementInfo :element="element" :type="type" :declarationLink="declarationLink" />
        </div>
        <div>
          <DsfrButtonGroup :buttons="actionButtons" inlineLayoutWhen="md" align="center" class="mb-8" />

          <DsfrModal :opened="!!modalToOpen" :title="modalTitle" :actions="modalActions" @close="closeModal">
            <template #default>
              <DsfrInput v-model="notes" label="Notes" label-visible is-textarea />
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
import { getApiType } from "@/utils/mappings"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"
import ElementInfo from "./ElementInfo"

const props = defineProps({ type: String, id: String })

const declarationId = computed(() => element.value?.declaration)
const declarationLink = computed(() => {
  if (!declarationId.value) return
  return { name: "InstructionPage", params: { declarationId: declarationId.value } }
})

const breadcrumbLinks = computed(() => {
  const links = [
    { to: { name: "DashboardPage" }, text: "Tableau de bord" },
    { to: { name: "InstructionDeclarations" }, text: "Déclarations pour instruction" },
  ]
  if (declarationLink.value) links.push({ to: declarationLink.value, text: "Instruction" })
  links.push({ text: "Demande d'ajout d'ingrédient" })
  return links
})

// Init
const url = computed(() => `/api/v1/declared-elements/${getApiType(props.type)}s/${props.id}`)
const { data: element, response, execute } = useFetch(url, { immediate: false }).get().json()

const getElementFromApi = async () => {
  await execute()
  await handleError(response)
}

getElementFromApi()
watch(element, (newElement) => {
  if (newElement) {
    const name = newElement.newName || `${newElement.newSpecies} ${newElement.newGenre}`
    document.title = `${name} - Compl'Alim`
  }
})

// Actions
const modalToOpen = ref(false)
const closeModal = () => (modalToOpen.value = false)

const notes = ref()

const openModal = (type) => {
  return () => {
    if (!notes.value) notes.value = element.value?.requestPrivateNotes
    modalToOpen.value = type
  }
}
const actionButtons = [
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
]

const updateElement = async (payload) => {
  const { data, response } = await useFetch(url, {
    headers: headers(),
  })
    .patch(payload)
    .json()
  handleError(response)
  if (data) {
    element.value = data.value
  }
}

const modals = {
  info: {
    title: "L’ajout du nouvel ingrédient nécessite plus d’information.",
    actions: [
      {
        label: "Enregistrer",
        onClick() {
          updateElement({
            requestStatus: "INFORMATION",
            requestPrivateNotes: notes.value || "",
          }).then(closeModal)
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
          updateElement({
            requestStatus: "REJECTED",
            requestPrivateNotes: notes.value || "",
          }).then(closeModal)
        },
      },
    ],
  },
}
const modalTitle = computed(() => modals[modalToOpen.value]?.title)

const modalActions = computed(() => {
  const actions = modals[modalToOpen.value]?.actions || []
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

const alerts = computed(() => ({
  REQUESTED: {
    title: "Nouvel ingrédient",
    description: "Ingrédient non intégré dans la base de données et en attente de validation.",
    type: "info",
  },
  INFORMATION: {
    title: "En attente d'information",
    description: element.value?.requestPrivateNotes,
    type: "warning",
  },
  REJECTED: {
    title: "Ingrédient refusé",
    description: element.value?.requestPrivateNotes,
    type: "error",
  },
}))
const alert = computed(() => alerts.value[element.value?.requestStatus])
</script>
