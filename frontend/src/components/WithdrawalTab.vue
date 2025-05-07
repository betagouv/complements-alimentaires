<template>
  <div>
    <h2>Retirer du marché</h2>
    <p>
      Votre produit « {{ declaration.name }} » a été déclaré. Vous pouvez néanmoins signaler son arrêt de
      commercialisation en cliquant ci-dessous. Veuillez noter que cette opération est irreversible.
    </p>
    <h3 class="fr-h5">Date effective du retrait du marché</h3>
    <DsfrRadioButtonSet v-model="chosenDateOption" :options="dateOptions" label="Date effective de retrait du marché" />
    <DsfrInputGroup v-if="chosenDateOption === 'other'" :error-message="firstErrorMsg(v$, 'effectiveDate')">
      <DsfrInput
        type="date"
        label="Date effective de retrait du marché"
        class="max-w-52 ml-8 mb-10 -mt-6"
        v-model="otherDate"
        required
      />
    </DsfrInputGroup>
    <DsfrButton secondary label="Retirer ce complément" @click="openModal" />

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
import { ref, computed } from "vue"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"
import { isoToPrettyDate } from "@/utils/date"
import { useVuelidate } from "@vuelidate/core"
import { errorRequiredField, firstErrorMsg } from "@/utils/forms"
import useToaster from "@/composables/use-toaster"

const declaration = defineModel()
const $externalResults = ref({})
const confirmationModalOpened = ref(false)
const emit = defineEmits("withdraw")

const withdrawDeclaration = async () => {
  const url = `/api/v1/declarations/${declaration.value.id}/withdraw/`
  const payload = { effectiveWithdrawalDate: effectiveDate.value }
  const { response } = await useFetch(url, { headers: headers() }).post(payload).json()
  $externalResults.value = await handleError(response)

  if (response.value.ok) {
    useToaster().addSuccessMessage("Votre produit a été retiré du marché")
    emit("withdraw")
  }
}

// Gestion de la date effective de retrait du marché
const today = new Date()
const chosenDateOption = ref(`${today}`)
const otherDate = ref()

// NOTE: Le champ DLUO est un champ de texte. Certaines déclarations ne contiennent donc pas un
// champ parseable en int (p.e « 24 à 36 mois selon les lots », « exempté » ou « Voir l'emballage »
const dluoDate = computed(() => {
  const dluoIsNumeric = /^\d+$/.test(declaration.value?.minimumDuration)
  if (!dluoIsNumeric) return

  const months = parseInt(declaration.value.minimumDuration)
  if (!months) return

  const afterDluo = new Date(today.getTime())
  afterDluo.setMonth(afterDluo.getMonth() + months)
  if (afterDluo.getDate() != today.getDate()) afterDluo.setDate(0)
  return afterDluo
})

const dateOptions = computed(() => {
  const options = [
    {
      label: `Aujourd'hui (${isoToPrettyDate(today)})`,
      value: `${today}`,
    },
  ]
  if (dluoDate.value)
    options.push({
      label: `Aujourd'hui + DLUO (${isoToPrettyDate(dluoDate.value)})`,
      hint: `Vous avez spécifié une durabilité minimale / DLUO de ${declaration.value.minimumDuration} mois`,
      value: `${dluoDate.value}`,
    })
  options.push({
    label: "Une autre date (à spécifier)",
    value: "other",
  })
  return options
})

const effectiveDate = computed(() => (chosenDateOption.value === "other" ? otherDate.value : chosenDateOption.value))
const rules = { effectiveDate: errorRequiredField }
const v$ = useVuelidate(rules, { effectiveDate }, { $externalResults })

const openModal = () => {
  v$.value.$clearExternalResults()
  v$.value.$validate()
  if (v$.value.$error) return
  confirmationModalOpened.value = true
}
</script>
