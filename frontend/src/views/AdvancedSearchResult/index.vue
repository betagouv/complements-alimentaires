<template>
  <div class="fr-container mb-10">
    <DsfrBreadcrumb
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { to: previousRoute, text: 'Recherche avancée' },
        { text: declaration?.name || 'Résultat' },
      ]"
    />
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else>
      <div class="sm:flex">
        <div class="flex-1">
          <h1 class="fr-text--sm font-normal mb-0!">Résultat de la recherche</h1>
          <h2 class="mb-1!">{{ declaration?.name }}</h2>
          <DsfrTag
            small
            v-if="declaration?.status"
            :label="statusProps[declaration.status].label"
            :icon="statusProps[declaration.status].icon"
            :class="declaration.status"
          />
        </div>
        <div v-if="showOpenButton" class="self-center flex gap-4">
          <DsfrButton
            v-if="isInstructor"
            secondary
            icon="ri-edit-fill"
            size="sm"
            label="Ouvrir dans la page instruction"
            @click="router.push({ name: 'InstructionPage', params: { declarationId: declaration?.id } })"
          />
          <DsfrButton
            v-if="isVisor"
            secondary
            icon="ri-file-edit-fill"
            size="sm"
            label="Ouvrir dans la page visa"
            @click="router.push({ name: 'VisaPage', params: { declarationId: declaration?.id } })"
          />
        </div>
      </div>
      <DeclarationSummary class="mt-4" :readonly="true" v-if="declaration" v-model="declaration" />
    </div>
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { onMounted, computed } from "vue"
import { useRouter } from "vue-router"
import { storeToRefs } from "pinia"
import { useRootStore } from "@/stores/root"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import { statusProps } from "@/utils/mappings"

import DeclarationSummary from "@/components/DeclarationSummary"
import { setDocumentTitle } from "@/utils/document"

const store = useRootStore()
const { loggedUser } = storeToRefs(store)

store.fetchDeclarationFieldsData()

const showOpenButton = computed(() => isInstructor.value || isVisor.value)
const isInstructor = computed(() => loggedUser.value?.globalRoles?.some((x) => x.name === "InstructionRole"))
const isVisor = computed(() => loggedUser.value?.globalRoles?.some((x) => x.name === "VisaRole"))

const router = useRouter()
const previousRoute = computed(() => {
  const previousRoute = router.getPreviousRoute().value
  return previousRoute?.name === "AdvancedSearchPage" ? previousRoute : { name: "AdvancedSearchPage" }
})

const props = defineProps({
  declarationId: String,
})

// Requêtes
const {
  response: declarationResponse,
  data: declaration,
  isFetching,
  execute: executeDeclarationFetch,
} = useFetch(`/api/v1/declarations/${props.declarationId}`, { immediate: false }).get().json()

onMounted(async () => {
  await executeDeclarationFetch()
  handleError(declarationResponse)
  setDocumentTitle([declaration.value.name, "Résultat de recherche"])
})
</script>
