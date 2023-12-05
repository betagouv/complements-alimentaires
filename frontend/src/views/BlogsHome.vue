<template>
  <div class="pt-10 bg-indigo-50 relative min-h-[160px]">
    <div class="fr-container">
      <h1 class="mb-2">Nos articles</h1>
      <p>Découvrez notre espace blog et témoignages</p>
    </div>
    <div class="absolute top-0 right-0 hidden md:block">
      <svg width="500" height="136" viewBox="0 0 500 136" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M671.466 44.0002C668.715 38.1372 662.411 28.1162 657.405 23.27C651.117 17.1815 643.421 11.9767 634.72 8.16223C624.749 3.79119 609.181 0.692853 597.802 0.0690516C586.423 -0.554229 573.991 7.0521 568.467 14.9258C565.798 18.7305 565 23.0002 565 23.0002C565 23.0002 559.725 18.6367 553.538 16.8681C533.71 11.1995 515.642 12.1303 495.352 16.6683C475.061 21.2065 464.241 37.4205 453 51.5002C447.251 44.6803 413.974 41.922 403.957 44.0708C374.487 50.3924 362.057 64.5382 349.546 86.5195C333.508 84.3004 317.007 82.6275 301.347 86.3716C296.666 87.4908 270.977 102.409 277.025 107.728C267.972 99.7647 252.99 96.9738 239.728 99.1997C226.466 101.426 214.902 108.095 206.169 116.278C207.113 115.394 180.359 111.554 177.625 111.51C166.426 111.326 155.142 113.792 145.742 118.613C137.019 123.087 129.25 129.682 118.915 130.629C112.921 131.177 106.966 129.692 100.975 129.127C90.9069 128.177 80.4626 129.912 71.7343 133.983C69.0736 135.224 66.5417 136.686 63.6404 137.527C57.4528 139.322 50.6206 138.065 44.0587 137.563C30.2939 136.511 9.29747 138.056 0 147.266C9.14899 144.287 13.9498 151.018 21.9406 153.564C30.9812 156.446 41.1049 157.04 50.7546 156.608C65.8115 155.933 80.6878 153.001 95.7644 153.303C119.207 153.772 141.294 161.986 164.532 164.466C196.159 167.841 228.331 160.469 260.075 163.072C282.463 164.909 303.852 171.65 326.243 173.467C354.193 175.735 382.074 170.247 409.824 166.771C448.54 161.922 488.037 160.968 527.056 163.94C575.274 167.613 624.279 177.208 671.466 168.56C677.271 167.496 683.708 165.689 686.045 161.363C687.383 158.885 687.061 156.065 686.601 153.396C685.511 147.061 683.78 140.795 681.435 134.676C679.866 130.58 675.042 123.784 675.704 119.425C679.566 93.9864 682.741 68.0294 671.466 44.0002Z"
          class="fill-indigo-200"
        />
      </svg>
    </div>
  </div>
  <div class="fr-container my-10">
    <div class="flex justify-center" v-if="loading">
      <ProgressSpinner />
    </div>
    <p v-else-if="blogPostCount === 0">Nous n'avons pas encore d'articles de blog</p>
    <div v-else>
      <div class="grid grid-cols-12">
        <DsfrCard
          class="col-span-12 sm:col-span-6 md:col-span-4 mb-4 mr-4"
          v-for="post in visibleBlogPosts"
          :key="post.id"
          :title="post.title"
          :detail="blogDate(post)"
          :description="blogDescription(post)"
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
const loading = computed(() => blogPostCount.value === null)
const blogDate = (post) => {
  return new Date(post.displayDate).toLocaleDateString("fr-FR", {
    year: "numeric",
    month: "short",
    day: "numeric",
  })
}
const blogDescription = (post) => post.body?.substring(0, 100).replace(/<\/?[^>]+(>|$)/g, "")

// Route management
watch(route, () => {
  visibleBlogPosts.value = null
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
div >>> .fr-card__desc {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
div >>> .fr-card__detail {
  margin-bottom: 6px;
}
div >>> .fr-pagination__list {
  justify-content: center;
}
</style>
