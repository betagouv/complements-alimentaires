<template>
  <div>
    <DsfrButton
      secondary
      icon="ri-mail-forbid-line"
      size="sm"
      label="Je n'ai pas reçu d'email"
      @click="opened = true"
      ref="modalOrigin"
    />
    <DsfrModal
      :actions="actions"
      ref="modal"
      :opened="opened"
      @close="close"
      title="E-mail de vérification non reçu ?"
      icon="ri-mail-forbid-line"
    >
      <p>
        Si vous n'avez pas reçu d'email au bout de quelques minutes, veuillez vérifier l'adresse e-mail entrée, ainsi
        que vos courriers indésirables. Sinon, cliquez sur le bouton ci-dessous pour recevoir un nouvel e-mail.
      </p>
    </DsfrModal>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import useToaster from "@/composables/use-toaster"

const props = defineProps({ userId: String })
const opened = ref(false)

const close = () => (opened.value = false)

// Main request definition
const url = computed(() => `/api/v1/send-new-signup-verification-email/${props.userId}`)
const { response, execute } = useFetch(url, {
  immediate: false,
}).json()

const resendEmail = async () => {
  await execute()
  await handleError(response)
  if (response.value.ok) {
    useToaster().addSuccessMessage("L'email de vérification a été renvoyé.")
  }
  close()
}

const actions = [
  {
    label: "Renvoyer un nouvel e-mail",
    onClick: resendEmail,
  },
  {
    label: "Annuler",
    onClick: close,
    secondary: true,
  },
]
</script>
