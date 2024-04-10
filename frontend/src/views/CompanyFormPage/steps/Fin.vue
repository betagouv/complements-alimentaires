<template>
  <div>
    <DsfrButton :label="`Accéder à « ${storedSocialName} »`" @click="goToCompany" />
  </div>
</template>

<script setup>
import { useCreateCompanyStore } from "@/stores/createCompany"

const { storedId, storedSocialName } = useCreateCompanyStore()

const goToCompany = () => {
  console.log("TODO: go to company ", storedId)
}
</script>
