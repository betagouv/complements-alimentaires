<template>
  <div>
    <DsfrButton v-if="!emailNotReceived" size="sm" label="Je n'ai pas reçu d'email" @click="emailNotReceived = true" />
    <template v-if="emailNotReceived">
      <p>
        Si vous n'avez pas reçu d'email au bout de quelques minutes, veuillez vérifier l'adresse e-mail entrée, ainsi
        que vos courriers indésirables. Sinon, cliquez sur le bouton ci-dessous pour recevoir un nouvel e-mail :
      </p>
      <DsfrButton
        size="sm"
        label="Renvoyer un e-mail de vérification"
        :disabled="isFetching || isFinished"
        @click="resendEmail"
      />
    </template>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import useToaster from "@/composables/use-toaster"

const props = defineProps({ userId: Number })

const emailNotReceived = ref(false)

// Main request definition
const url = computed(() => `/api/v1/send-new-signup-verification-email/${props.userId}`)
const { response, execute, isFetching, isFinished } = useFetch(url, {
  immediate: false,
}).json()

const resendEmail = async () => {
  await execute()
  await handleError(response)
  if (response.value.ok) {
    useToaster().addSuccessMessage("L'email de vérification a été renvoyé.")
  }
}
</script>
