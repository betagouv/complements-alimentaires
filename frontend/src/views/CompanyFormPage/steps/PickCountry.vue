<template>
  <div>
    <FormWrapper class="max-w-xl mx-auto">
      <DsfrInputGroup>
        <CountryField
          v-model="country"
          description="Dans quel pays l'entreprise est-elle immatriculée ?"
          @update:modelValue="onCountrySelected"
        />
      </DsfrInputGroup>
    </FormWrapper>
  </div>
</template>

<script setup>
import { ref, onActivated } from "vue"
import FormWrapper from "@/components/FormWrapper"
import CountryField from "@/components/fields/CountryField"
import { useCreateCompanyStore } from "@/stores/createCompany"

// Props & emits
const emit = defineEmits(["changeStep"])

const country = ref(undefined)

const onCountrySelected = (selectedOption) => {
  const identifierType = selectedOption == "FR" ? "siret" : "vat"
  useCreateCompanyStore().setCompanyCountryAndIdentifierType(selectedOption, identifierType) // pour créer l'entreprise plus tard en ayant l'information
  emit("changeStep", {
    name: `Identification par n° ${identifierType.toUpperCase()}`,
    component: "Identification",
  })
}

onActivated(() => {
  // remet à 0 le pays choisi pour qu'en cliquant précédent, le choix du pays déclenche de nouveau le passage à l'étape suivante
  country.value = undefined
})
</script>
