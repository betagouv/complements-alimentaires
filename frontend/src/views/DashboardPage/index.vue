<template>
  <div class="fr-container my-8">
    <template v-if="isSupervisor">
      <h2 class="fr-h5">
        <v-icon class="mr-1 mb-[3px]" name="ri-home-2-fill" />
        Gestion d'entreprise
      </h2>
      <ActionGrid :actions="supervisorActions" />
    </template>

    <template v-if="isDeclarant">
      <h2 class="fr-h5 !mt-8">
        <v-icon class="mr-1 mb-[3px]" name="ri-capsule-fill" />
        Mes déclarations
      </h2>
      <ActionGrid :actions="declarantActions" />
    </template>

    <template v-if="emptyRoles">
      <h2 class="fr-h5 !mt-8">Démarrez chez Compl-Alim !</h2>
      <ActionGrid :actions="onboardingActions" />
    </template>

    <h2 class="fr-h5 !mt-8">
      <v-icon class="mr-1 mb-[3px]" name="ri-account-circle-line" />
      Mon compte
    </h2>
    <ActionGrid :actions="userActions" />
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import ActionGrid from "./ActionGrid"

const store = useRootStore()
const { loggedUser } = storeToRefs(store)

const emptyRoles = computed(() => !loggedUser.value.roles || loggedUser.value.roles.length === 0)
const isSupervisor = computed(() => loggedUser.value.roles.some((x) => x.name === "CompanySupervisor"))
const isDeclarant = computed(() => loggedUser.value.roles.some((x) => x.name === "Declarant"))

const supervisorActions = [
  {
    title: "Les déclartions de mes entreprises",
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
    description: "Renseignez les données de votre entreprise pour effetuer vos déclarations",
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
  },
]
</script>
