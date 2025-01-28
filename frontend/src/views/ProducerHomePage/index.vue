<template>
  <div>
    <SearchBlock />

    <div class="fr-container my-6 md:my-16">
      <DeclarationBlock />
    </div>

    <div class="fr-container my-10">
      <Suspense><WebinarBlock /></Suspense>
    </div>
    <div class="bg-blue-france-975">
      <div class="fr-container py-6 md:py-10">
        <NewsletterBlock />
      </div>
    </div>
  </div>
</template>
<script setup>
import NewsletterBlock from "@/views/LandingPage/NewsletterBlock"
import DeclarationBlock from "@/views/ProducerHomePage/DeclarationBlock"
import WebinarBlock from "@/views/LandingPage/WebinarBlock"
import SearchBlock from "@/views/ProducerHomePage/SearchBlock"
</script>
