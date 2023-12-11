<template>
  <SearchBlock />

  <div class="fr-container my-6 md:my-16">
    <DeclarationBlock />
  </div>

  <div class="bg-blue-france-975">
    <div class="fr-container p-6 md:p-10">
      <NewsletterBlock />
    </div>
  </div>
</template>
<script setup>
import NewsletterBlock from "@/views/LandingPage/NewsletterBlock.vue"
import DeclarationBlock from "@/views/LandingPage/DeclarationBlock.vue"
import SearchBlock from "@/views/LandingPage/SearchBlock.vue"
</script>
