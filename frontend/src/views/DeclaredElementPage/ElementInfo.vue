<template>
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
</template>

<script setup>
import { computed } from "vue"
import { getTypeIcon, getTypeInFrench } from "@/utils/mappings"

const props = defineProps({ element: Object, type: String, declarationLink: Object })

// prepare template data for display
const icon = computed(() => getTypeIcon(props.type))
const typeName = computed(() => getTypeInFrench(props.element?.newType || props.type))

const franceAuthorization = computed(() => {
  return props.element?.authorizationMode === "FR"
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
    { label: "Libellé", key: "newName" },
    { label: "Description", key: "newDescription" },
  ],
}

const elementProfile = computed(() => {
  if (!props.element) return []

  const items = []

  const detail = detailForType[props.type] || detailForType.default
  detail.forEach((d) => {
    items.push({ label: d.label, text: props.element[d.key] })
  })

  if (franceAuthorization.value === false) {
    items.push(
      ...[
        {
          label: "Pays de référence",
          text: props.element.euReferenceCountry,
        },
        {
          label: "Source réglementaire",
          text: props.element.euLegalSource,
          href: props.element.euLegalSource,
        },
      ]
    )
  }
  return items
})
</script>
