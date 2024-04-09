<template>
  <div>
    <DsfrAlert size="sm">
      L'entreprise
      <strong>{{ storedSocialName }}</strong>
      avec le SIRET
      <strong>{{ storedSiret }}</strong>
      fait déjà partie des entreprises dont vous êtes le gestionnaire.

      <!-- TODO: changer la redirection quand la page d'entreprise particulière existe -->
      <div class="mt-4">
        <DsfrButton :label="`Accéder à « ${storedSocialName} »`" @click="$router.push({ name: 'DashboardPage' })" />
      </div>
    </DsfrAlert>
  </div>
</template>

<script setup>
import { useCreateCompanyStore } from "@/stores/createCompany"

const { storedSiret, storedSocialName } = useCreateCompanyStore()
</script>
