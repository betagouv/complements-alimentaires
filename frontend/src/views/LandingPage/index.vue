<template>
  <TaglineBlock />

  <div class="fr-container my-10">
    <MissionBlock />
  </div>

  <StatsBlock />

  <div class="fr-container my-10">
    <BlogBlock />
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
import TaglineBlock from "@/views/LandingPage/TaglineBlock"
import WebinarBlock from "@/views/LandingPage/WebinarBlock"
import BlogBlock from "@/views/LandingPage/BlogBlock"
import StatsBlock from "@/views/LandingPage/StatsBlock"
import MissionBlock from "@/views/LandingPage/MissionBlock"
</script>
