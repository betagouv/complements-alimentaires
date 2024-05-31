<template>
  <div class="fr-container mb-8 flex flex-col">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Mes informations personnelles' }]"
    />
    <EditPersonalInformationBlock />
    <hr class="mt-14 mb-4" />
    <ChangePasswordBlock />
    <hr class="mt-14 mb-4" />
    <DeleteAccountBlock />
  </div>
</template>

<script setup>
import EditPersonalInformationBlock from "./EditPersonalInformationBlock"
import ChangePasswordBlock from "./ChangePasswordBlock"
import DeleteAccountBlock from "./DeleteAccountBlock"
</script>
