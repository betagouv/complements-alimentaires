<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[
        { to: '/', text: 'Accueil' },
        { to: '/blog', text: 'Articles de blog' },
        { text: blogPost?.title || '' },
      ]"
    />
  </div>
  <div v-if="blogPost" class="fr-container my-8">
    <h1 class="fr-h4">{{ blogPost.title }}</h1>
    <p class="my-0">{{ author }}</p>
    <p class="fr-text--xs my-0">{{ date }}</p>
    <div id="content" v-html="blogPost.body" class="text-left"></div>
  </div>
</template>

<script setup>
import { computed, watch } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"

const props = defineProps({
  id: String,
})

const { data: blogPost, response, execute } = useFetch(`/api/v1/blogPosts/${props.id}`, { immediate: false }).json()
const fetchBlogPost = async () => {
  await execute()
  await handleError(response)
}

const date = computed(() => {
  if (!blogPost.value) return null
  return new Date(blogPost.value.displayDate).toLocaleDateString("fr-FR", {
    year: "numeric",
    month: "short",
    day: "numeric",
  })
})
const author = computed(() => {
  if (!blogPost.value?.author) return null
  return `${blogPost.value.author.firstName} ${blogPost.value.author.lastName}`
})

// init
fetchBlogPost()

watch(blogPost, (post) => {
  if (post) document.title = `${post.title} - Compl'Alim`
})
</script>

<style scoped>
#content >>> img {
  max-width: 100%;
  height: auto;
}
</style>
