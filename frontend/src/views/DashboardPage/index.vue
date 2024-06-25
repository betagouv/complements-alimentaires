<template>
  <div>
    <RoleBarBlock
      @changeCompany="onChangeCompany"
      :name="loggedUser.firstName"
      :companies="companies"
      :activeCompany="company"
    />
    <div class="fr-container my-8 flex flex-col gap-8">
      <ActionGrid
        v-if="isSupervisorForActiveCompany"
        :actions="supervisorActions"
        :title="`Gestion de l'entreprise ${company.socialName}`"
        icon="ri-home-4-line"
      />
      <ActionGrid v-if="isDeclarant" :actions="declarantActions" title="Mes déclarations" icon="ri-capsule-fill" />
      <ActionGrid v-if="isInstructor" :actions="instructionActions" title="Instruction" icon="ri-survey-fill" />
      <ActionGrid v-if="isVisor" :actions="visorActions" title="Visa / Signature" icon="ri-file-search-fill" />
      <ActionGrid v-if="emptyRoles" :actions="onboardingActions" title="Démarrez chez Compl-Alim !" />
      <ActionGrid :actions="userActions" title="Mon compte" icon="ri-account-circle-line" />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import ActionGrid from "./ActionGrid"
import RoleBarBlock from "./RoleBarBlock"
import { useRoute } from "vue-router"
import { useRouter } from "vue-router"

const store = useRootStore()
const router = useRouter()
const route = useRoute()
const { loggedUser, companies } = storeToRefs(store)

const company = computed(() => companies.value?.find((c) => +c.id === +route.query.company))
const isSupervisor = computed(() => companies?.value.some((c) => c.roles?.some((x) => x.name === "SupervisorRole")))
const isDeclarant = computed(() => companies?.value.some((c) => c.roles?.some((x) => x.name === "DeclarantRole")))
const isInstructor = computed(() => loggedUser.value?.globalRoles.some((x) => x.name === "InstructionRole"))
const isVisor = computed(() => loggedUser.value?.globalRoles.some((x) => x.name === "VisaRole"))
const emptyRoles = computed(() => !isSupervisor.value && !isDeclarant.value && !isInstructor.value)

const isSupervisorForActiveCompany = computed(() => company.value?.roles?.some((x) => x.name === "SupervisorRole"))

// Si on voulait lier le bloc délcarant.e à l'entreprise active, on pourrait utiliser cette
// computed var dans le v-if de ce bloc
// const isDeclarantForActiveCompany = computed(() => company.value?.roles?.some((x) => x.name === "DeclarantRole"))

// Sélectionne une entreprise si l'user est un superviseur et qu'on n'a pas le queryparam
onMounted(() => {
  const hasInvalidCompanyParam = route.query.company && !company.value
  if (hasInvalidCompanyParam || !route.query.company) {
    const query = companies.value?.length ? { company: companies.value[0].id } : {}
    router.replace({ query })
  }
})

const onChangeCompany = (id) => router.push({ query: { company: id } })

const supervisorActions = computed(() => [
  {
    title: "Les déclarations de mon entreprise",
    description: "Visualisez et gérez les déclarations de votre entreprise",
    link: { name: "CompanyDeclarationsPage", params: { id: company.value?.id } },
  },
  {
    title: "Les collaborateurs de mon entreprise",
    description: "Gérez les différents collaborateurs, leurs rôles, les demandes, et invitez-en des nouveaux",
    link: { name: "CollaboratorsPage", params: { id: company.value?.id } },
  },
  {
    title: "Les coordonnées de l'entreprise",
    description: "Consultez et mettez à jour les données de votre entreprise",
    link: { name: "CompanyPage", params: { id: company.value?.id } },
  },
])

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

const instructionActions = [
  {
    title: "Liste des déclarations",
    description: "Accédez à la liste des déclarations Compl'Alim",
    link: { name: "InstructionDeclarations" },
  },
]

const visorActions = [
  {
    title: "Déclarations à viser",
    description: "Consultez la liste des déclarations attendant une validation",
    link: { name: "VisaDeclarations" },
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
  {
    title: "Nouvelle entreprise",
    description: "Créez ou rejoignez une nouvelle entreprise",
    link: { name: "CompanyFormPage" },
  },
]
</script>
