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
        les 3 mois l'ensemble des données personnelles relatives à votre compte, conformément à la réglementation en
        vigueur.
      </p>
    </DsfrModal>

    <SectionTitle title="Supprimer mon compte" icon="ri-user-unfollow-line" />
    <DsfrButton size="sm" class="!bg-red-marianne-425" label="Supprimer" @click="opened = true" />
  </div>
</template>

<script setup>
import { ref } from "vue"
import SectionTitle from "@/components/SectionTitle"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import useToaster from "@/composables/use-toaster"
import { headers } from "@/utils/data-fetching"
import { logOut } from "@/utils/auth"

const opened = ref(false)
const close = () => (opened.value = false)

// Main request definition
const { response, execute } = useFetch(
  `/api/v1/delete-user`,
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
    useToaster().addMessage({
      type: "success",
      title: "Compte supprimé",
      description: "Votre compte a bien été supprimé.",
    })
  }
  close()
  await logOut()
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
