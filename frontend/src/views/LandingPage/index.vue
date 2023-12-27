<template>
  <div class="fr-container my-10">
    <DeclarationBlock />
  </div>

  <div class="bg-blue-france-975">
    <div class="fr-container p-6 md:p-10">
      <NewsletterBlock />
    </div>
  </div>

  <div class="fr-container my-10">
    <WebinarBlock />
  </div>
</template>
<script setup>
import NewsletterBlock from "@/views/LandingPage/NewsletterBlock.vue"
import DeclarationBlock from "@/views/LandingPage/DeclarationBlock.vue"
import WebinarBlock from "@/views/LandingPage/WebinarBlock.vue"
</script>
