<template>
  <div>
    <DsfrAlert type="success">
      <div>L'entreprise « {{ modelValue.socialName }} » a bien été créée et vous en avez les droits de gestion.</div>
      <div class="mt-4 flex gap-x-4">
        <DsfrButton :label="`Accéder à « ${modelValue.socialName} »`" @click="goToCompany" />
        <DsfrButton label="Retour au tableau de bord" tertiary @click="$router.push({ name: 'DashboardPage' })" />
      </div>
    </DsfrAlert>
  </div>
</template>

<script setup>
// Props & emits
const props = defineProps({ modelValue: Object })

const goToCompany = () => {
  console.log("TODO: go to company ", props.modelValue.id)
}
</script>
