<template>
  <div class="fr-container my-10">
    <h1 class="pb-6">Notre espace blog</h1>
    <div class="flex justify-center" v-if="loading">
      <ProgressSpinner />
    </div>
    <p v-else-if="blogPostCount === 0">Nous n'avons pas encore d'articles de blog</p>
    <div v-else>
      <div class="grid grid-cols-12">
        <DsfrCard
          class="col-span-12 sm:col-span-6 md:col-span-4 m-4"
          v-for="post in visibleBlogPosts"
          :key="post.id"
          :title="post.title"
        />
      </div>
      <DsfrPagination @update:currentPage="updatePage" :pages="pages" :current-page="page - 1" :truncLimit="5" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref, watch } from "vue"
import { verifyResponse } from "@/utils"
import { useRoute, useRouter } from "vue-router"
import ProgressSpinner from "@/components/ProgressSpinner"

const route = useRoute()
const router = useRouter()

// Pagination
const limit = 6
const page = ref(null)
const blogPostCount = ref(null)
const offset = computed(() => (page.value - 1) * limit)
const pages = computed(function () {
  const totalPages = Math.ceil(blogPostCount.value / limit)
  const pages = []
  for (let i = 0; i < totalPages; i++)
    pages.push({
      label: i + 1,
      href: `${route.path}?page=${i + 1}`,
      title: `Page ${i + 1}`,
    })
  return pages
})
const updatePage = (newPage) => (page.value = newPage + 1)
watch(page, updateRoute)

// Blog posts
const visibleBlogPosts = ref(null)
function fetchCurrentPage() {
  let url = `/api/v1/blogPosts/?limit=${limit}&offset=${offset.value}`
  return fetch(url)
    .then(verifyResponse)
    .then((response) => {
      visibleBlogPosts.value = response.results
      blogPostCount.value = response.count
    })
    .catch(() => {
      window.alert("Une erreur est survenue veuillez réessayer plus tard")
    })
}
const loading = computed(function () {
  return blogPostCount.value === null
})

// Route management
watch(route, function () {
  visibleBlogPosts.value = null
  populateParametersFromRoute()
  fetchCurrentPage()
})
function populateParametersFromRoute() {
  page.value = route.query.page ? parseInt(route.query.page) : 1
}
function updateRoute() {
  const query = { page: page.value }
  if (route.query.page) router.push({ query }).catch(() => {})
  else router.replace({ query }).catch(() => {})
}

onMounted(() => {
  populateParametersFromRoute()
  if (Object.keys(route.query).length > 0) fetchCurrentPage()
})
</script>
