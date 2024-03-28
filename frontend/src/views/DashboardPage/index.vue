<template>
  <DsfrNotice>
    <div class="flex md:items-center flex-col md:flex-row md:justify-between">
      <p>Bienvenue, {{ firstName }}</p>
      <div class="flex gap-x-2 -mr-12">
        <DsfrTag
          v-for="displayName in roleNames"
          :key="displayName"
          :label="displayName"
          icon="ri-account-circle-line"
          class="flex gap-x-1 border border-gray-300 uppercase"
          small
        />
      </div>
    </div>
  </DsfrNotice>
  <div class="fr-container my-8 flex flex-col gap-8">
    <ActionGrid
      v-if="isCompanySupervisor"
      :actions="supervisorActions"
      title="Gestion d'entreprise"
      icon="ri-home-4-line"
    />
    <ActionGrid v-if="isDeclarant" :actions="declarantActions" title="Mes déclarations" icon="ri-capsule-fill" />
    <ActionGrid v-if="emptyRoles" :actions="onboardingActions" title="Démarrez chez Compl-Alim !" />
    <ActionGrid :actions="userActions" title="Mon compte" icon="ri-account-circle-line" />
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import ActionGrid from "./ActionGrid"

const store = useRootStore()
const { loggedUser } = storeToRefs(store)

const firstName = computed(() => loggedUser.value.firstName)
const roleNames = computed(() => loggedUser.value.roles.map((role) => role.displayName))

const emptyRoles = computed(() => !loggedUser.value.roles || loggedUser.value.roles.length === 0)
const isCompanySupervisor = computed(() => loggedUser.value.roles.some((x) => x.name === "CompanySupervisor"))
const isDeclarant = computed(() => loggedUser.value.roles.some((x) => x.name === "Declarant"))

const supervisorActions = [
  {
    title: "Les déclarations de mes entreprises",
    description: "Visualisez et gérez les déclarations de votre entreprise",
  },
  {
    title: "Modifier mes coordonnées",
    description: "Consultez et mettez à jour les données de votre entreprise",
  },
  {
    title: "Nouvelle entreprise",
    description: "Créez ou rejoignez une nouvelle entreprise",
  },
]

const declarantActions = [
  {
    title: "Créer une nouvelle déclaration",
    description: "Démarrez une nouvelle déclaration pour votre complément alimentaire",
    link: { name: "ProducerFormPage" },
  },
  {
    title: "Toutes mes déclarations",
    description: "Consultez, modifiez ou dupliquez une déclaration que vous avez effectuée",
  },
]

const onboardingActions = [
  {
    title: "Créez ou rejoignez une entreprise",
    description: "Renseignez les données de votre entreprise pour effectuer vos déclarations",
  },
  {
    title: "Contactez notre équipe",
    description: "Une question ? Contactez-nous",
  },
]

const userActions = [
  {
    title: "Mes informations personnelles",
    description: "Consultez et mettez à jour vos informations personnelles",
    link: "/informations-personnelles",
  },
]
</script>
