<template>
  <div>
    <div class="flex justify-between">
      <div>
        <SectionTitle :title="`Collaborateurs actuels de ${company.socialName}`" icon="ri-user-3-line" />
        <div class="flex flex-col"></div>
        <p>Gérez ici l'ensemble des collaborateurs et leurs rôles.</p>
      </div>
      <div>
        <DsfrButton label="Aide sur les rôles" icon="ri-question-line" size="sm" tertiary />
      </div>
    </div>

    <div v-for="user in staff" :key="user.id">
      <div class="flex items-center">
        <v-icon class="size-5" name="ri-user-follow-line" />
        <div class="ml-2">
          <div>
            {{ user.firstName }} {{ user.lastName }}
            <span class="text-xs" v-if="user.id === loggedUser.id">(vous)</span>
          </div>
          <div class="text-xs">{{ user.email }}</div>
        </div>
        <div class="ml-2 md:ml-8 flex flex-col gap-y-1">
          <div class="flex gap-x-2">
            <RoleTag v-for="role in user.roles" :key="role.name" :role="role" :show-actions="true" />
          </div>
          <DsfrButton
            v-if="canRoleBeAddedTo(user)"
            label="Ajouter un rôle"
            icon="ri-add-circle-line"
            tertiary
            no-outline
            size="sm"
            class="!pl-0"
          />
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

const store = useRootStore()
const { loggedUser, company } = storeToRefs(store)

const canRoleBeAddedTo = (user) => user.roles.length < 2 // TODO: très simple pour le moment, à modifier.

const url = computed(() => `/api/v1/companies/${company.value.id}/staff`)
const { data: staff, response, execute } = useFetch(url, { immediate: false }).json()

onMounted(async () => {
  await execute()
  await handleError(response)
})
</script>
