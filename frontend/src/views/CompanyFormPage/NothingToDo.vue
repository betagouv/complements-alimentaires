<template>
  <div>
    <DsfrAlert size="sm">
      L'entreprise
      <strong>{{ storedSocialName }}</strong>
      avec le n° {{ storedIdentifierType.toUpperCase() + " " }}
      <strong>{{ storedIdentifier }}</strong>
      fait déjà partie des entreprises dont vous êtes le gestionnaire.

      <!-- TODO: changer la redirection quand la page d'entreprise particulière existe -->
      <div class="mt-4 flex gap-x-4">
        <DsfrButton :label="`Accéder à « ${storedSocialName} »`" @click="goToCompany" />
        <DsfrButton label="Retour au tableau de bord" tertiary @click="$router.push({ name: 'DashboardPage' })" />
      </div>
    </DsfrAlert>
  </div>
</template>

<script setup>
import { useCreateCompanyStore } from "@/stores/createCompany"

const { storedIdentifier, storedIdentifierType, storedId, storedSocialName } = useCreateCompanyStore()

const goToCompany = () => {
  console.log("TODO: go to company ", storedId)
}
</script>
