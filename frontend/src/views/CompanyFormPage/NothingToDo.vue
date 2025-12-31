<template>
  <div>
    <DsfrAlert>
      <p>
        L'entreprise
        <strong>{{ company.socialName }}</strong>
        avec le n° {{ company.identifierType.toUpperCase() + " " }}
        <strong>{{ company.identifier }}</strong>
        fait déjà partie des entreprises dont vous êtes le gestionnaire.
      </p>
      <!-- TODO: changer la redirection quand la page d'entreprise particulière existe -->
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
