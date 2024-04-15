<template>
  <div>
    <DsfrAlert type="success">
      <div>L'entreprise « {{ storedSocialName }} » a bien été créée et vous en avez les droits de gestion.</div>
      <div class="mt-4 flex gap-x-4">
        <DsfrButton :label="`Accéder à « ${storedSocialName} »`" @click="goToCompany" />
        <DsfrButton label="Retour au tableau de bord" tertiary @click="$router.push({ name: 'DashboardPage' })" />
      </div>
    </DsfrAlert>
  </div>
</template>

<script setup>
import { useCreateCompanyStore } from "@/stores/createCompany"

const { storedId, storedSocialName } = useCreateCompanyStore()

const goToCompany = () => {
  console.log("TODO: go to company ", storedId)
}
</script>
