<template>
  <div v-if="blogPosts && blogPosts.length > 0">
    <h3>Les ressources nouvellement ajoutées</h3>
    <div class="mb-4 text-right">
      <router-link :to="{ name: 'BlogsHome' }">
        Voir toutes les ressources
        <v-icon scale="0.75" class="ml-1" name="ri-arrow-right-line" />
      </router-link>
    </div>

    <div class="grid grid-cols-12 gap-4">
      <BlogCard class="col-span-12 sm:col-span-6 md:col-span-4" v-for="post in blogPosts" :key="post.id" :post="post" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { verifyResponse } from "@/utils"
import BlogCard from "@/components/BlogCard"

const blogPosts = ref(null)

onMounted(() => {
  const url = "/api/v1/blogPosts/?limit=3&offset=0"
  return fetch(url)
    .then(verifyResponse)
    .then((response) => (blogPosts.value = response.results))
    .catch(() => {
      window.alert("Une erreur est survenue veuillez réessayer plus tard")
    })
})
</script>
