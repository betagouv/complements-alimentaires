<template>
  <div>
    <h2>Retirer du marché</h2>
    <p>
      Votre produit « {{ declaration.name }} » a été autorisé. Vous pouvez néanmoins déclarer son arrêt de
      commercialisation en cliquant ci-dessous. Veuillez noter que cette opération est irreversible.
    </p>
    <DsfrButton secondary label="Retirer ce complément" @click="confirmationModalOpened = true" />

    <DsfrModal title="Veuillez confirmer" :opened="confirmationModalOpened" @close="confirmationModalOpened = false">
      <p>Êtes-vous sûr de vouloir retirer ce produit du marché ?</p>
      <div class="flex gap-4">
        <DsfrButton secondary label="Non" @click="confirmationModalOpened = false" />
        <DsfrButton label="Oui, je veux le retirer" @click="withdrawDeclaration" />
      </div>
    </DsfrModal>
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { ref } from "vue"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"

const declaration = defineModel()
const $externalResults = ref({})
const confirmationModalOpened = ref(false)
const emit = defineEmits("withdraw")

const withdrawDeclaration = async () => {
  const url = `/api/v1/declarations/${declaration.value.id}/withdraw/`
  const { response } = await useFetch(url, { headers: headers() }).post().json()
  $externalResults.value = await handleError(response)

  if (response.value.ok) {
    useToaster().addSuccessMessage("Votre produit a été retiré du marché")
    emit("withdraw")
  }
}
</script>
