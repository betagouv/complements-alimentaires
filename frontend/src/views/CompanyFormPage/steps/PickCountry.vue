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
  useCreateCompanyStore().setCompanyCountry(selectedOption) // pour créer l'entreprise plus tard en ayant l'information
  emit("changeStep", {
    index: 1,
    name: selectedOption == "FR" ? "Identification par SIRET" : "Identification par n° de TVA intracommunautaire",
    component: selectedOption == "FR" ? "IdentificationBySiret" : "IdentificationByVat",
    goToNextStep: true,
  })
}

onActivated(() => {
  // remet à 0 le pays choisi pour qu'en fassant précédent, le choix du pays déclenche de nouveau le passage à l'étape suivante
  country.value = undefined
})
</script>
