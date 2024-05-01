<template>
  <div>
    <div class="flex justify-between">
      <div>
        <SectionTitle :title="`Collaborateurs actuels de ${company.socialName}`" icon="ri-user-line" />
        <div class="flex flex-col"></div>
        <p>Gérez ici l'ensemble des collaborateurs et leurs rôles.</p>
      </div>
      <div>
        <DsfrButton label="Aide sur les rôles" icon="ri-question-line" size="sm" tertiary />
      </div>
    </div>

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
      <hr class="mt-4 -mb-2 border" />
    </div>
    <DsfrButton label="Inviter un nouveau collaborateur" icon="ri-mail-add-line" size="sm" />
  </div>
</template>

<script setup>
import { onMounted, computed } from "vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import SectionTitle from "@/components/SectionTitle"
import RoleTag from "@/components/RoleTag.vue"
import { headers } from "@/utils/data-fetching"
import { roleNameDisplayNameMapping } from "@/utils/mappings"

const store = useRootStore()
const { loggedUser, company } = storeToRefs(store)

const canRoleBeAddedTo = (roleName, user) => !user.roles.some((role) => role.name === roleName)

// Requête initiale pour récupérer les collaborateurs de l'entreprise
const collaboratorsUrl = computed(() => `/api/v1/companies/${company.value.id}/collaborators`)
const {
  data: collaborators,
  response: collaboratorsResponse,
  execute: collaboratorsExecute,
} = useFetch(collaboratorsUrl, { immediate: false }).json()

onMounted(async () => {
  await collaboratorsExecute()
  await handleError(collaboratorsResponse)
})

// Requête pour modifier les rôles d'un utilisateur pour une entreprise donnée
const changeRole = async (roleName, user, action) => {
  const url = `${collaboratorsUrl.value}/${user.id}/${roleName}/${action}/`
  const { response, data: collaboratorUpdatedLine } = await useFetch(url, { headers: headers() }).patch().json()
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
