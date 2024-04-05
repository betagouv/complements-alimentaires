<template>
  <div class="fr-container my-8">
    <DsfrCallout class="space-y-4" title="E-mail de vérification envoyé">
      <p>
        Un e-mail vient d'être envoyé à
        <strong>{{ email }}</strong>
        <br />
        Veuillez cliquez dans le lien à l'intérieur pour vérifier votre adresse e-email et pouvoir utiliser votre
        compte.
      </p>
      <SendNewSignupVerificationEmail :userId="userId" />
    </DsfrCallout>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router"
import SendNewSignupVerificationEmail from "@/components/SendNewSignupVerificationEmail"

const { userId, email } = useRoute().query
</script>
