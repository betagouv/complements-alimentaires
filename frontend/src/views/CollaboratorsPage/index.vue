<template>
  <div class="fr-container mb-8 flex flex-col">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Gestion des collaborateurs' }]"
    />

    <div class="flex justify-between">
      <SectionTitle :title="`Collaborateurs actuels de ${company.socialName}`" icon="ri-user-line" />
      <AddNewCollaborator
        :companyId="company.id"
        :disabled="requestOngoing"
        @added="() => ongoingInvitationsExecute() && collaboratorsExecute()"
      />
    </div>
    <p>Gérez ici l'ensemble des collaborateurs et leurs rôles.</p>

    <div v-for="user in collaborators" :key="user.id">
      <div class="flex items-center">
        <v-icon class="size-5" name="ri-user-follow-line" />
        <div class="ml-2">
          <div>
            {{ user.firstName }} {{ user.lastName }}
            <span class="text-xs" v-if="user.id === loggedUser.id">(vous)</span>
          </div>
          <div class="text-xs">{{ user.email }}</div>
        </div>
        <div class="ml-2 md:ml-8 flex gap-x-2">
          <div class="flex gap-x-2 items-center">
            <RoleTag
              v-for="role in user.roles"
              :key="role.name"
              :role="role"
              :show-actions="!(role.name == 'SupervisorRole' && user.id == loggedUser.id)"
              @remove="changeRole(role.name, user, 'remove')"
            />
          </div>
          <template v-for="(roleDisplayName, roleName) in roleNameDisplayNameMapping">
            <DsfrButton
              :key="roleName + user.id"
              v-if="canRoleBeAddedTo(roleName, user)"
              @click="changeRole(roleName, user, 'add')"
              :label="`Attribuer rôle ${roleDisplayName}`"
              icon="ri-add-circle-line"
              tertiary
              no-outline
              size="sm"
            />
          </template>
        </div>
      </div>
      <hr class="mt-4 -mb-2" />
    </div>
    <ClaimsBlock
      class="mt-8"
      :solicitations="solicitations"
      @process="() => solicitationsExecute() && collaboratorsExecute()"
    />
    <SolicitationsHolder
      v-if="ongoingInvitations"
      title="Invitations envoyées"
      icon="ri-chat-upload-line"
      :solicitations="ongoingInvitations"
      emptyText="Vous n'avez envoyé aucune invitation."
      :actions="[]"
      showRecipientEmail
    />
  </div>
</template>

<script setup>
import { onMounted, computed } from "vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import SectionTitle from "@/components/SectionTitle"
import RoleTag from "@/components/RoleTag"
import { headers } from "@/utils/data-fetching"
import { roleNameDisplayNameMapping } from "@/utils/mappings"
import ClaimsBlock from "./ClaimsBlock"
import SolicitationsHolder from "./SolicitationsHolder"
import AddNewCollaborator from "./AddNewCollaborator"
import { useRoute } from "vue-router"

const route = useRoute()
const store = useRootStore()
const { loggedUser, companies } = storeToRefs(store)

const company = computed(() => companies.value?.find((c) => +c.id === +route.params.id))
const canRoleBeAddedTo = (roleName, user) => !user.roles.some((role) => role.name === roleName)

const rootUrl = computed(() => `/api/v1/companies/${company.value.id}`)
const params = { immediate: false }

// Requête initiale pour récupérer les collaborateurs de l'entreprise
const {
  data: collaborators,
  response: collaboratorsResponse,
  execute: collaboratorsExecute,
  isFetching: collaboratorsIsFetching,
} = useFetch(`${rootUrl.value}/collaborators`, params).json()

// Requête pour obtenir les invitations en cours
const {
  data: ongoingInvitations,
  response: ongoingInvitationsResponse,
  execute: ongoingInvitationsExecute,
  isFetching: ongoingInvitationsIsFetching,
} = useFetch(`${rootUrl.value}/collaboration-invitations/`, params).json()

// Requête pour obtenir les demandes / solicitations
const {
  data: solicitations,
  response: solicitationsResponse,
  execute: solicitationsExecute,
  isFetching: solicitationsIsFetching,
} = useFetch(`${rootUrl.value}/company-access-claims/`, params).json()

const requestOngoing = computed(
  () => collaboratorsIsFetching.value || ongoingInvitationsIsFetching.value || solicitationsIsFetching.value
)

onMounted(async () => {
  await collaboratorsExecute()
  await ongoingInvitationsExecute()
  await solicitationsExecute()
  await handleError(collaboratorsResponse)
  await handleError(ongoingInvitationsResponse)
  await handleError(solicitationsResponse)
})

// Requête pour modifier les rôles d'un utilisateur pour une entreprise donnée
const changeRole = async (roleName, user, action) => {
  const url = `/api/v1/users/${user.id}/${action}-role/`
  const payload = { companyPk: company.value.id, roleName: roleName }
  const { response, data: collaboratorUpdatedLine } = await useFetch(url, { headers: headers() }).post(payload).json()
  await handleError(response)
  if (response.value.ok) {
    // mise à jour de l'UI sur la ligne concernée
    collaborators.value = collaborators.value
      .map((obj) => {
        if (obj.id === user.id) {
          if (collaboratorUpdatedLine.value.roles.length > 0) {
            return collaboratorUpdatedLine.value
          }
          // si l'utilisateur n'a plus aucun rôle, il n'est plus considéré comme un collaborateur, et disparait
          return null
        }
        return obj
      })
      .filter((obj) => obj !== null) // retire les objets marqués null
    store.fetchInitialData()
  }
}
</script>
