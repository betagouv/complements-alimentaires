<template>
  <SearchBlock />

  <div class="fr-container my-6 md:my-16">
    <DeclarationBlock />
  </div>

  <div class="fr-container my-10">
    <WebinarBlock />
  </div>
  <div class="bg-blue-france-975">
    <div class="fr-container p-6 md:p-10">
      <NewsletterBlock />
    </div>
  </div>
</template>
<script setup>
import NewsletterBlock from "@/views/LandingPage/NewsletterBlock"
import DeclarationBlock from "@/views/ProducersPage/DeclarationBlock"
import WebinarBlock from "@/views/LandingPage/WebinarBlock"
import SearchBlock from "@/views/ProducersPage/SearchBlock"
</script>
