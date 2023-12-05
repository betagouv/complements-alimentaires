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
    <h1 class="fr-h4">Blog post {{ blogPost.title }}</h1>
    <p class="my-0">{{ author }}</p>
    <p class="fr-text--xs my-0">{{ date }}</p>
    <div id="content" v-html="blogPost.body" class="text-left"></div>
  </div>
  <DsfrErrorPage v-else-if="notFound" class="my-8" title="Article non trouvé" />
</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue"
import { verifyResponse, NotFoundError } from "@/utils"

const props = defineProps({
  id: String,
})

const blogPost = ref(null)
const notFound = ref(false)

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

watch(blogPost, (post) => {
  if (post) document.title = `${post.title} - Compléments alimentaires`
})

onMounted(() => {
  return fetch(`/api/v1/blogPosts/${props.id}`)
    .then(verifyResponse)
    .then((response) => (blogPost.value = response))
    .catch((error) => {
      if (error instanceof NotFoundError) notFound.value = true
      else window.alert("Une erreur est survenue veuillez réessayer plus tard")
    })
})
</script>

<style scoped>
#content >>> img {
  max-width: 100%;
  height: auto;
}
</style>
