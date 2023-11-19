<template>
  <div class="fr-container my-10">
    <DeclarationBlock />
  </div>

  <div class="bg-slate-100">
    <div class="fr-container p-6 md:p-10">
      <NewsletterBlock />
    </div>
  </div>
</template>
<script setup>
import NewsletterBlock from "@/views/LandingPage/NewsletterBlock.vue"
import DeclarationBlock from "@/views/LandingPage/DeclarationBlock.vue"
</script>
