<template>
  <div>
    <DsfrAlert type="success">
      <div>
        Votre demande a bien été envoyée. Veuillez patienter. Vous recevrez un e-mail lorsque celle-ci aura été traitée.
      </div>
      <DsfrButton
        class="mt-4"
        label="Retour au tableau de bord"
        tertiary
        @click="$router.push({ name: 'DashboardPage' })"
      />
    </DsfrAlert>
  </div>
</template>
