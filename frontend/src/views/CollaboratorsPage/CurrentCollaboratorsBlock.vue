<template>
  <div>
    <div class="flex justify-between">
      <div>
        <SectionTitle :title="`Collaborateurs actuels de ${company.socialName}`" icon="ri-user-line" />
        <p>Gérez ici l'ensemble des collaborateurs et leurs rôles.</p>
      </div>
      <div>
        <DsfrButton @click="opened = true" label="Ajouter un nouveau collaborateur" icon="ri-user-add-line" size="sm" />
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
  </div>

  <!-- Modale d'ajout d'un nouveau collaborateur -->
  <DsfrModal
    :actions="actions"
    ref="modal"
    :opened="opened"
    @close="opened = false"
    title="Ajouter un nouveau collaborateur"
    icon="ri-user-add-line"
  >
    <DsfrInputGroup>
      <DsfrInput
        v-model="email"
        label="Entrez l'adresse e-mail de votre collaborateur :"
        labelVisible
        type="email"
        autocomplete="email"
        spellcheck="false"
        class="max-w-md"
      />
    </DsfrInputGroup>
    <DsfrCheckboxSet
      v-model="selectedRoles"
      :options="selectableRoles"
      small
      legend="Sélectionnez un ou plusieurs rôles qui lui seront attribués :"
    />
  </DsfrModal>
</template>

<script setup>
import { onMounted, computed, ref } from "vue"
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

// Modal d'ajout d'un nouvel utilisateur
const opened = ref(false)
const submitAddNewCollaborator = () => {}
const actions = [
  {
    label: "Valider",
    onClick: submitAddNewCollaborator,
  },
  {
    label: "Annuler",
    onClick: () => {
      opened.value = false
    },
    secondary: true,
  },
]
// TODO: isoler l'ajout d'un colab dans un component à part ?
const email = ref("")
const selectedRoles = ref([])
const selectableRoles = [
  {
    label: roleNameDisplayNameMapping.DeclarantRole,
    name: "DeclarantRole",
    hint: "permet au collaborateur de créer et gérer ses propres déclarations.",
  },
  {
    label: roleNameDisplayNameMapping.SupervisorRole,
    name: "SupervisorRole",
    hint: "permet au collaborateur de gérer l'ensemble de l'entreprise (les déclarations existantes, les collaborateurs, et l'entreprise elle-même).",
  },
]
</script>
