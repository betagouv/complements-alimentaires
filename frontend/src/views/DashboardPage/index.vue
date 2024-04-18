<template>
  <RoleBarBlock :name="loggedUser.firstName" :roles="loggedUser.roles" />
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
import RoleBarBlock from "./RoleBarBlock"

const store = useRootStore()
const { loggedUser } = storeToRefs(store)

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
    link: { name: "CompanyFormPage" },
  },
]

const declarantActions = [
  {
    title: "Créer une nouvelle déclaration",
    description: "Démarrez une nouvelle déclaration pour votre complément alimentaire",
    link: { name: "NewDeclaration" },
  },
  {
    title: "Toutes mes déclarations",
    description: "Consultez, modifiez ou dupliquez une déclaration que vous avez effectuée",
    link: { name: "DeclarationsHomePage" },
  },
]

const onboardingActions = [
  {
    title: "Créez ou rejoignez une entreprise",
    description: "Renseignez les données de votre entreprise pour effectuer vos déclarations",
    link: { name: "CompanyFormPage" },
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
    link: { name: "UserAccountPage" },
  },
]
</script>
