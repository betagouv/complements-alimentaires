<template>
  <div class="pt-10 bg-blue-france-975 relative min-h-[160px]">
    <div class="fr-container">
      <h1 class="mb-2">Nos ressources</h1>
      <p>Apprenez plus de la reglementation et de notre plateforme avec nos infolettres et articles.</p>
    </div>
    <img class="hidden md:block absolute bottom-0 right-20" src="/static/images/plants.png" alt="" />
  </div>
  <div class="fr-container my-6">
    <div v-if="isFetching" class="flex justify-center">
      <ProgressSpinner />
    </div>
    <template v-if="data">
      <div v-if="data.results.length > 0">
        <div class="grid grid-cols-12 gap-4">
          <BlogCard
            class="col-span-12 sm:col-span-6 md:col-span-4"
            v-for="post in data.results"
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
      <p v-else>Nous n'avons pas encore de ressources</p>
    </template>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import ProgressSpinner from "@/components/ProgressSpinner"
import BlogCard from "@/components/BlogCard"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { getPagesForPagination } from "@/utils/components"
import { setDocumentTitle } from "@/utils/document"

const route = useRoute()
const router = useRouter()

// Pagination
const limit = 6
const page = ref(null)
const offset = computed(() => (page.value - 1) * limit)
const pages = computed(() => getPagesForPagination(data.value.count, limit, route.path))

const updatePage = (newPage) => (page.value = newPage + 1)
const updateRoute = () => {
  const query = { page: page.value }
  if (route.query.page) router.push({ query }).catch(() => {})
  else router.replace({ query }).catch(() => {})
}
watch(page, updateRoute)

// Blog posts
const url = computed(() => `/api/v1/blog-post/?limit=${limit}&offset=${offset.value}`)
const { data, response, execute, isFetching } = useFetch(url, { immediate: false }).json()

const fetchCurrentPage = async () => {
  await execute()
  await handleError(response)
  setDocumentTitle(["Ressources"], {
    number: page.value,
    total: pages.value.length,
    term: "page",
  })
}

// Route management
watch(route, () => {
  populateParametersFromRoute()
  fetchCurrentPage()
})
const populateParametersFromRoute = () => {
  page.value = route.query.page ? parseInt(route.query.page) : 1
}

// Init
populateParametersFromRoute()
if (Object.keys(route.query).length > 0) fetchCurrentPage()
</script>

<style scoped>
/* Affichage des deux premières lignes du corps de l'article */
div :deep(.fr-card__desc) {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
div :deep(.fr-card__detail) {
  margin-bottom: 6px;
}
</style>
