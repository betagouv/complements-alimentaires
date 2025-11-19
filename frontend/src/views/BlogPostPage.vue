<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: '/', text: 'Accueil' }, { to: '/blog', text: 'Ressources' }, { text: blogPost?.title || '' }]"
    />
  </div>
  <div v-if="blogPost" class="fr-container my-8">
    <div class="p-4 border mb-4">
      <h1 class="fr-h4 mb-2!">{{ blogPost.title }}</h1>
      <p class="mb-0!">{{ author }}</p>
      <p class="fr-text--xs mb-0!">{{ date }}</p>
    </div>
    <div id="content" v-html="blogPost.content" class="text-left"></div>
  </div>
</template>

<script setup>
import { computed, watch } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { setDocumentTitle } from "@/utils/document"

const props = defineProps({
  id: String,
})

const { data: blogPost, response, execute } = useFetch(`/api/v1/blog-post/${props.id}`, { immediate: false }).json()
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
  if (post) setDocumentTitle([post.title])
})
</script>

<style scoped>
#content :deep(img) {
  max-width: 100%;
  height: auto;
}
</style>
