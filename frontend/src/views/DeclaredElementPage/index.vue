<template>
  <div>
    <DsfrNotice title="Page en construction" />
    <DsfrNotice
      title="NOUVEL INGRÉDIENT"
      desc="Ingrédient non intégré dans la base de donnée et en attente de validation. "
    />
    <div class="fr-container">
      <DsfrBreadcrumb class="mb-8" :links="breadcrumbLinks" />
      <div class="grid grid-cols-2 gap-4">
        <div class="bg-grey-975 py-4 px-4 mb-8">
          <p class="mt-6">
            <v-icon :name="icon" />
            {{ typeName }}
          </p>
          <div class="grid grid-cols-2">
            <p :aria-hidden="true" class="fr-h4">{{ authorizationInfo.flag }}</p>
            <p class="content-center">{{ authorizationInfo.text }}</p>
          </div>
          <div v-for="(info, idx) in elementProfile" :key="idx" class="grid grid-cols-2">
            <p>
              <b>{{ info.label }}</b>
            </p>
            <p v-if="info.href">
              <a :href="info.href" _target="blank" rel="noopener">{{ info.text }}</a>
              <!-- TODO: open in new icon -->
            </p>
            <p v-else>{{ info.text }}</p>
          </div>
          <div class="grid justify-items-end">
            <router-link :to="declarationLink">
              Voir la déclaration
              <v-icon icon="ri-arrow-right-line"></v-icon>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from "vue"
import { getTypeIcon, getTypeInFrench, getApiType } from "@/utils/mappings"
import { useFetch } from "@vueuse/core"

const props = defineProps({ type: String, id: Number })
const icon = computed(() => getTypeIcon(props.type))
const typeName = computed(() => getTypeInFrench(element.value?.newType || props.type))

const url = computed(() => `/api/v1/declared-elements/${getApiType(props.type)}s/${props.id}`)
const { data: element, response, execute } = useFetch(url, { immediate: false }).get().json()
// TODO: handle 404 and 403

const franceAuthorization = computed(() => {
  return element.value?.authorizationMode === "FR"
})
const authorizationInfo = computed(() => {
  return {
    flag: franceAuthorization.value ? "🇫🇷" : "🇪🇺",
    text: franceAuthorization.value ? "Autorisé en France." : "Autorisé dans un état membre de l’EU ou EEE.",
  }
})

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

// Init
execute()
watch(element, (newElement) => {
  if (newElement) {
    const name = newElement.newName || `${newElement.newSpecies} ${newElement.newGenre}`
    document.title = `${name} - Compl'Alim`
  }
})

const declarationId = computed(() => element.value?.declaration)
const declarationLink = computed(() => {
  if (!declarationId.value) return
  return { name: "InstructionPage", params: { declarationId: declarationId.value } }
})

const breadcrumbLinks = computed(() => {
  const links = [{ to: { name: "InstructionDeclarations" }, text: "Déclarations pour instruction" }]
  if (declarationLink.value) links.push({ to: declarationLink.value, text: "Instruction" })
  links.push({ text: "Demande d'ajout d'ingrédient" })
  return links
})
</script>
