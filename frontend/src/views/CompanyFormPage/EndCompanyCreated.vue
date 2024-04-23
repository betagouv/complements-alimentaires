<template>
  <div>
    <DsfrAlert type="success">
      <div>L'entreprise « {{ company.socialName }} » a bien été créée et vous en avez les droits de gestion.</div>
      <div class="mt-4 flex gap-x-4">
        <DsfrButton :label="`Accéder à « ${company.socialName} »`" @click="goToCompany" />
        <DsfrButton label="Retour au tableau de bord" tertiary @click="$router.push({ name: 'DashboardPage' })" />
      </div>
    </DsfrAlert>
  </div>
</template>

<script setup>
const company = defineModel()

const goToCompany = () => {
  console.log("TODO: go to company ", company.value.id)
}
</script>
