<template>
  <div>
    <DsfrButton :label="`Accéder à « ${storedSocialName} »`" />
  </div>
</template>

<script setup>
import { useCreateCompanyStore } from "@/stores/createCompany"

const { storedId, storedSocialName } = useCreateCompanyStore()
</script>
