<template>
  <div>
    <DsfrNotice title="En construction" desc="Des nouvelles fonctionnalités arrivent bientôt !" />
    <div class="fr-container">
      <DsfrBreadcrumb class="mb-8" :links="breadcrumbLinks" />
      <DsfrAlert
        title="Nouvel ingrédient"
        description="Ingrédient non intégré dans la base de données et en attente de validation."
        class="mb-4"
      />
      <div v-if="element">
        <div class="grid md:grid-cols-2 gap-4">
          <div class="bg-grey-975 p-4 mb-8">
            <p class="text-blue-france-sun-113">
              <v-icon :name="icon" />
              {{ typeName }}
            </p>
            <div class="grid grid-cols-3">
              <p :aria-hidden="true" class="fr-h2">{{ authorizationInfo.flag }}</p>
              <p class="content-center col-span-2">{{ authorizationInfo.text }}</p>
            </div>
            <div v-for="(info, idx) in elementProfile" :key="`element-profile-${idx}`" class="grid grid-cols-3">
              <p>
                <b>{{ info.label }}</b>
              </p>
              <p class="col-span-2">
                <a v-if="info.href" :href="info.href" target="_blank" rel="noopener" class="text-blue-france-sun-113">
                  {{ info.text }}
                </a>
                <span v-else>{{ info.text }}</span>
              </p>
            </div>
            <div class="grid justify-items-end p-2">
              <router-link :to="declarationLink" class="text-blue-france-sun-113">
                Voir la déclaration
                <v-icon icon="ri-arrow-right-line"></v-icon>
              </router-link>
            </div>
          </div>
        </div>
        <div>
          <DsfrButtonGroup :buttons="actionButtons" inlineLayoutWhen="md" align="center" class="mb-8" />

          <DsfrModal :opened="!!modalToOpen" :title="title" :actions="actions" @close="closeModal">
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
import { getTypeIcon, getTypeInFrench, getApiType } from "@/utils/mappings"
import { handleError } from "@/utils/error-handling"

const props = defineProps({ type: String, id: String })

// prepare template data for display
const icon = computed(() => getTypeIcon(props.type))
const typeName = computed(() => getTypeInFrench(element.value?.newType || props.type))

const franceAuthorization = computed(() => {
  return element.value?.authorizationMode === "FR"
})
const authorizationInfo = computed(() => {
  return {
    flag: franceAuthorization.value ? "🇫🇷" : "🇪🇺",
    text: franceAuthorization.value ? "Autorisé en France." : "Autorisé dans un état membre de l’EU ou EEE.",
  }
})

const detailForType = {
  plant: [
    { label: "Nom", key: "newName" },
    { label: "Description", key: "newDescription" },
  ],
  microorganism: [
    { label: "Genre", key: "newGenre" },
    { label: "Espèce", key: "newSpecies" },
    { label: "Description", key: "newDescription" },
  ],
  default: [
    { label: "Libillé", key: "newName" },
    { label: "Description", key: "newDescription" },
  ],
}

const elementProfile = computed(() => {
  if (!element.value) return []

  const items = []

  const detail = detailForType[props.type] || detailForType.default
  detail.forEach((d) => {
    items.push({ label: d.label, text: element.value[d.key] })
  })

  if (franceAuthorization.value === false) {
    items.push(
      ...[
        {
          label: "Pays de référence",
          text: element.value.euReferenceCountry,
        },
        {
          label: "Source réglementaire",
          text: element.value.euLegalSource,
          href: element.value.euLegalSource,
        },
      ]
    )
  }
  return items
})

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
const actionButtons = [
  {
    label: "Demander plus d’information",
    tertiary: true,
    onclick: () => (modalToOpen.value = "info"),
  },
  {
    label: "Refuser l’ingrédient",
    tertiary: true,
    "no-outline": true,
    icon: "ri-close-line",
    onclick: () => (modalToOpen.value = "refuse"),
  },
]

const modalToOpen = ref(false)
const closeModal = () => (modalToOpen.value = false)

const modals = {
  info: {
    title: "L’ajout d’un nouvel ingrédient nécessite plus d’information.",
    actions: [
      {
        label: "Enregistrer",
        onClick() {
          // TODO: update status and save note
          closeModal()
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
          // TODO: update status and save note
          closeModal()
        },
      },
    ],
  },
}

const title = computed(() => modals[modalToOpen.value]?.title)
// TODO: prefill with existing note?
const notes = ref()

const actions = computed(() => {
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
</script>
