<template>
  <div v-if="blogPosts.results.length > 0">
    <h3>Les ressources nouvellement ajoutées</h3>
    <div class="mb-4 text-right">
      <router-link :to="{ name: 'BlogsHome' }">
        Voir toutes les ressources
        <v-icon scale="0.75" class="ml-1" name="ri-arrow-right-line" />
      </router-link>
    </div>

    <div class="grid grid-cols-12 gap-4">
      <BlogCard
        class="col-span-12 sm:col-span-6 md:col-span-4"
        v-for="post in blogPosts.results"
        :key="post.id"
        :post="post"
      />
    </div>
  </div>
</template>

<script setup>
import BlogCard from "@/components/BlogCard"
import { useFetch } from "@vueuse/core"

const { data: blogPosts } = await useFetch("/api/v1/blogPosts/?limit=3&offset=0").json()
</script>
