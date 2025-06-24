<template>
  <div class="fr-container pb-8">
    <DsfrBreadcrumb
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Les entreprises' }]"
    />
    <DsfrAlert title="Page en construction" />
  </div>
</template>

<script setup></script>
