<template>
  <div class="fr-container">
    <DsfrBreadcrumb class="mb-8" :links="breadcrumbLinks" />

    <h1>
      <v-icon scale="2" :name="icon" />
      Modification élément
    </h1>
  </div>
</template>

<script setup>
import { /*ref, */ computed /*, watch*/ } from "vue"
import { getTypeIcon, /*getTypeInFrench,*/ unSlugifyType /*, getApiType*/ } from "@/utils/mappings"
// import { useRoute, useRouter } from "vue-router"
// import { useFetch } from "@vueuse/core"
// import { handleError } from "@/utils/error-handling"

const props = defineProps({ urlComponent: String })
const elementId = computed(() => props.urlComponent.split("--")[0])
const type = computed(() => unSlugifyType(props.urlComponent.split("--")[1]))
const icon = computed(() => getTypeIcon(type.value))

const breadcrumbLinks = computed(() => {
  const links = [{ to: { name: "DashboardPage" }, text: "Tableau de bord" }]
  links.push({ text: `Modification élément ${elementId.value}` })
  return links
})
</script>
