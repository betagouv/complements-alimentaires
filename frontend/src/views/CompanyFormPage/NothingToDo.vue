<template>
  <div>
    <DsfrAlert size="sm">
      L'entreprise
      <strong>{{ modelValue.socialName }}</strong>
      avec le n° {{ modelValue.identifierType.toUpperCase() + " " }}
      <strong>{{ modelValue.identifier }}</strong>
      fait déjà partie des entreprises dont vous êtes le gestionnaire.

      <!-- TODO: changer la redirection quand la page d'entreprise particulière existe -->
      <div class="mt-4 flex gap-x-4">
        <DsfrButton :label="`Accéder à « ${modelValue.socialName} »`" @click="goToCompany" />
        <DsfrButton label="Retour au tableau de bord" tertiary @click="$router.push({ name: 'DashboardPage' })" />
      </div>
    </DsfrAlert>
  </div>
</template>

<script setup>
const props = defineProps({ modelValue: Object })

const goToCompany = () => {
  console.log("TODO: go to company ", props.modelValue.id)
}
</script>
