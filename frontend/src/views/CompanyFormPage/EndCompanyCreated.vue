<template>
  <div>
    <DsfrAlert type="success">
      <p>L'entreprise « {{ company.socialName }} » a bien été créée et vous en avez les droits de gestion.</p>
      <div class="mt-4 flex gap-x-4">
        <DsfrButton
          :label="`Accéder à « ${company.socialName} »`"
          @click="$router.push({ name: 'CompanyPage', params: { id: company.id } })"
        />
        <DsfrButton label="Retour au tableau de bord" tertiary @click="$router.push({ name: 'DashboardPage' })" />
      </div>
    </DsfrAlert>
  </div>
</template>

<script setup>
const company = defineModel()
</script>
