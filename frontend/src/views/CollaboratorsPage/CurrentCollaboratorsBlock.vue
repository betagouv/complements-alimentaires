<template>
  <div>
    <div class="flex justify-between">
      <SectionTitle :title="`Collaborateurs actuels de ${company.socialName}`" icon="ri-user-line" />
      <div>
        <DsfrButton @click="opened = true" label="Ajouter un collaborateur" icon="ri-user-add-line" size="sm" />
      </div>
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
      <hr class="mt-4 -mb-2 border" />
    </div>
  </div>

  <!-- Modale d'ajout d'un collaborateur -->
  <DsfrModal
    :actions="actions"
    ref="modal"
    :opened="opened"
    @close="close"
    title="Ajouter un collaborateur"
    icon="ri-user-add-line"
  >
    <DsfrInputGroup :error-message="firstErrorMsg(v$, 'recipientEmail')">
      <DsfrInput
        v-model="state.recipientEmail"
        label="Entrez l'adresse e-mail de votre collaborateur :"
        labelVisible
        type="email"
        autocomplete="email"
        spellcheck="false"
        class="max-w-md"
      />
    </DsfrInputGroup>
    <DsfrCheckboxSet
      :error-message="firstErrorMsg(v$, 'selectedRoles')"
      v-model="state.selectedRoles"
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
import useVuelidate from "@vuelidate/core"
import useToaster from "@/composables/use-toaster"
import { errorRequiredField, errorRequiredEmail, firstErrorMsg } from "@/utils/forms"

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

//
// Modal d'ajout d'un nouvel utilisateur // TODO: isoler cette partie dans un component à part ?
//

const opened = ref(false)

// Form state & rules

const getInitialState = () => ({
  recipientEmail: "",
  selectedRoles: [],
})

const state = ref(getInitialState())

const rules = {
  recipientEmail: errorRequiredEmail,
  selectedRoles: errorRequiredField,
}

const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

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

const close = () => {
  opened.value = false
  // RAZ form state & Vuelidate validation state
  state.value = getInitialState()
  v$.value.$reset()
}

const submitInviteCollaborator = async () => {
  v$.value.$clearExternalResults()
  v$.value.$validate()
  if (v$.value.$error) {
    return
  }
  const url = `/api/v1/companies/${company.value.id}/collaboration-invitations/`
  const { response, data } = await useFetch(url, { headers: headers() })
    .post({ roles: state.value.selectedRoles, recipientEmail: state.value.recipientEmail })
    .json()
  $externalResults.value = await handleError(response)
  if (response.value.ok) {
    await collaboratorsExecute() // met à jour les collaborateurs existants, car ils peuvent avoir changé
    useToaster().addMessage({
      type: "success",
      // exceptionnellement on utilise le message directement du back, car plusieurs cas possibles
      description: data.value.message,
    })
    close()
  }
}

const actions = [
  {
    label: "Valider",
    onClick: submitInviteCollaborator,
  },
  {
    label: "Annuler",
    onClick: close,
    secondary: true,
  },
]
</script>
