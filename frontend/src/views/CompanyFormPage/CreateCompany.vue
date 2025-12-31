<template>
  <div>
    <DsfrAlert>
      <p>
        L'entreprise dont le n°
        {{ company.identifierType.toUpperCase() + " " }}
        est
        <strong>{{ company.identifier }}</strong>
        n'est pas encore enregistrée dans notre base de données. Pour ce faire, veuillez vérifier ou compléter les
        informations ci-dessous. À l'issue, vous en deviendrez automatiquement son gestionnaire.
      </p>
    </DsfrAlert>
    <CompanyForm
      class="mt-8"
      @responseReady="handleResponse"
      :initialState="initialState"
      :url="createCompanyUrl"
      method="post"
    />
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRootStore } from "@/stores/root"
import CompanyForm from "@/components/CompanyForm"

const rootStore = useRootStore()

// Props & emits
const company = defineModel()
const initialState = ref({
  socialName: company.value.siretData?.socialName || "",
  commercialName: "",
  address: company.value.siretData?.address || "",
  additionalDetails: "",
  postalCode: company.value.siretData?.postalCode || "",
  city: company.value.siretData?.city || "",
  cedex: company.value.siretData?.cedex || "",
  country: company.value.country,
  // on passe soit un numéro de SIRET, soit de TVA dans le payload
  [company.value.identifierType]: company.value.identifier,
  // activities
  activities: [],
  // contact
  phone_number: "",
  email: "",
  website: "",
})
const emit = defineEmits(["changeStep"])
const createCompanyUrl = "/api/v1/companies/"

// Gère la réponse du component enfant
const handleResponse = (data) => {
  if (data.value) {
    company.value.id = data.value.id
    company.value.socialName = data.value.socialName
    rootStore.fetchInitialData()
    emit("changeStep", {
      name: "L'entreprise a bien été créée",
      component: "EndCompanyCreated",
    })
  }
}
</script>
