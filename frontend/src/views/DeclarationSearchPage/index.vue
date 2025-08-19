<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { text: 'Recherche compléments alimentaires' },
      ]"
    />
    <h1 class="fr-h3">Tableau des compléments alimentaires</h1>
    <DeclarationsTableSection v-if="store.initialDataLoaded" />
  </div>
</template>

<script setup>
import DeclarationsTableSection from "@/components/NewBepiasViews/DeclarationsTableSection"
import { useRootStore } from "@/stores/root"

const store = useRootStore()
store.fetchDeclarationFieldsData()
</script>
