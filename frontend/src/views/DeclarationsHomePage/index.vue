<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Mes déclarations' }]"
    />
    <div class="block sm:flex items-center mb-8">
      <h1 class="!mb-0 grow">Mes déclarations</h1>
      <DsfrButton v-if="hasDeclarations" label="Nouvelle déclaration" secondary @click="createNewDeclaration" />
    </div>
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <DeclarationsTable :data="data" v-else-if="hasDeclarations" />
    <div v-else class="mb-8">
      <p>Vous n'avez pas encore créé des déclarations.</p>
      <DsfrButton icon="ri-capsule-fill" label="Créer ma première déclaration" @click="createNewDeclaration" />
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from "vue"
import ProgressSpinner from "@/components/ProgressSpinner"
import { handleError } from "@/utils/error-handling"
import DeclarationsTable from "./DeclarationsTable"
import { useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"

const store = useRootStore()
const { loggedUser } = storeToRefs(store)
const { response, data, isFetching } = useFetch(
  `/api/v1/users/${loggedUser.value.id}/declarations/?ordering=-modificationDate`
)
  .get()
  .json()

watch(response, () => handleError(response))

const hasDeclarations = computed(() => !!data.value?.length)

const router = useRouter()
const createNewDeclaration = () => router.push({ name: "NewDeclaration" })
</script>
