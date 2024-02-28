<template>
  <div class="pt-10 bg-blue-france-975 relative min-h-[160px]">
    <div class="fr-container">
      <h1 class="mb-2">Nos articles</h1>
      <p>Découvrez notre espace blog et témoignages</p>
    </div>
    <img class="hidden md:block absolute bottom-0 right-20" src="/static/images/plants.png" />
  </div>
  <div class="fr-container my-6">
    <div class="flex justify-center" v-if="loading">
      <ProgressSpinner />
    </div>
    <p v-else-if="blogPostCount === 0">Nous n'avons pas encore d'articles de blog</p>
    <div v-else>
      <div class="grid grid-cols-12 gap-4">
        <BlogCard
          class="col-span-12 sm:col-span-6 md:col-span-4"
          v-for="post in visibleBlogPosts"
          :key="post.id"
          :post="post"
        />
      </div>
      <DsfrPagination
        class="mt-4"
        @update:currentPage="updatePage"
        :pages="pages"
        :current-page="page - 1"
        :truncLimit="5"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref, watch } from "vue"
import { verifyResponse } from "@/utils/custom-errors"
import { useRoute, useRouter } from "vue-router"
import ProgressSpinner from "@/components/ProgressSpinner"
import BlogCard from "@/components/BlogCard"

const route = useRoute()
const router = useRouter()

// Pagination
const limit = 6
const page = ref(null)
const blogPostCount = ref(null)
const offset = computed(() => (page.value - 1) * limit)
const pages = computed(() => {
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
const fetchCurrentPage = () => {
  const url = `/api/v1/blogPosts/?limit=${limit}&offset=${offset.value}`
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
const loading = computed(() => blogPostCount.value === null)

// Route management
watch(route, () => {
  populateParametersFromRoute()
  fetchCurrentPage()
})
const populateParametersFromRoute = () => {
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

<style scoped>
/* Affichage des deux premières lignes du corps de l'article */
div >>> .fr-card__desc {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
div >>> .fr-card__detail {
  margin-bottom: 6px;
}
</style>
