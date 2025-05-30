<template>
  <TaglineBlock />

  <div class="fr-container my-10">
    <MissionBlock />
  </div>

  <Suspense>
    <div>
      <div class="fr-container my-10">
        <BlogBlock />
      </div>

      <div class="fr-container my-10">
        <WebinarBlock />
      </div>
    </div>
  </Suspense>

  <div class="bg-blue-france-975">
    <div class="fr-container py-6 md:py-10">
      <NewsletterBlock />
    </div>
  </div>
</template>

<script setup>
import NewsletterBlock from "@/views/LandingPage/NewsletterBlock"
import TaglineBlock from "@/views/LandingPage/TaglineBlock"
import WebinarBlock from "@/views/LandingPage/WebinarBlock"
import BlogBlock from "@/views/LandingPage/BlogBlock"
import MissionBlock from "@/views/LandingPage/MissionBlock"
</script>
