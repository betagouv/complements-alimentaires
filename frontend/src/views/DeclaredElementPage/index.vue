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
                <div v-if="changeCrossType">
                  <!-- TODO: reuse fields for a demand of this type (for new_name/new_species etc) -->
                  <ElementDetail :objectType="replacement.objectType" v-model="additionalInfo" />
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
import { getApiType } from "@/utils/mappings"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"
import ElementInfo from "./ElementInfo"
import ElementAlert from "./ElementAlert"
import ReplacementSearch from "./ReplacementSearch"
import ElementDetail from "@/components/ElementDetail"

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
const url = computed(() => `/api/v1/declared-elements/${getApiType(props.type)}/${props.id}`)
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

const replacement = ref()
// TODO: objectType does not work for other ingredients - need to do API mapping?
const changeCrossType = computed(() => replacement.value?.objectType !== element.value.type)
const additionalInfo = ref({})
watch(replacement, () => {
  additionalInfo.value = JSON.parse(JSON.stringify(element.value))
})

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
            }
            // TODO: clear search if we stay on page
            updateElement("replace", payload).then(closeModal)
          },
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
            updateElement("reject", {
              requestPrivateNotes: notes.value || "",
            }).then(closeModal)
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
