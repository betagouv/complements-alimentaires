<template>
  <div>
    <DsfrModal
      :actions="actions"
      ref="modal"
      :opened="opened"
      @close="close"
      title="Supprimer votre compte ?"
      icon="ri-user-unfollow-line"
    >
      <p>
        Votre compte sera immédiatemment désactivé (vous ne pourrez plus vous connecter). Nous supprimerons ensuite dans
        les meilleurs délais l'ensemble des données personnelles relatives à votre compte.
      </p>
    </DsfrModal>

    <SectionTitle title="Supprimer mon compte" icon="ri-user-unfollow-line" class="text-red-marianne-425!" />
    <DsfrButton size="sm" label="Supprimer" @click="opened = true" />
  </div>
</template>

<script setup>
import { ref } from "vue"
import SectionTitle from "@/components/SectionTitle"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"
import { logOut } from "@/utils/auth"
import { useRootStore } from "@/stores/root"

const store = useRootStore()
const opened = ref(false)
const close = () => (opened.value = false)

// Main request definition
const { response, execute } = useFetch(
  `/api/v1/users/${store.loggedUser.id}`,
  { headers: headers() },
  {
    immediate: false,
  }
)
  .delete()
  .json()

const deleteAccount = async () => {
  await execute()
  await handleError(response)
  if (response.value.ok) {
    await logOut("Votre compte a bien été supprimé.")
  }
  close()
}

const actions = [
  {
    label: "Supprimer mon compte",
    onClick: deleteAccount,
  },
  {
    label: "Annuler",
    onClick: close,
    secondary: true,
  },
]
</script>
