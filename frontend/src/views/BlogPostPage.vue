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
  <!-- TODO: replace with error management feature from backend -->
  <!-- <DsfrErrorPage v-else-if="notFound" class="my-8" title="Article non trouvé" /> -->
</template>

<script setup>
import { computed, watch } from "vue"
import { useFetch } from "@vueuse/core"
import useToaster from "@/composables/use-toaster"

const props = defineProps({
  id: String,
})

const { data: blogPost, execute, error } = useFetch(`/api/v1/blogPosts/${props.id}`, { immediate: false }).json()
const fetchBlogPost = async () => {
  await execute()
  if (error.value) useToaster().addUnknownErrorMessage()
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
  if (post) document.title = `${post.title} - Compléments alimentaires`
})
</script>

<style scoped>
#content >>> img {
  max-width: 100%;
  height: auto;
}
</style>
