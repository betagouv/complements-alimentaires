<template>
  <div class="fr-container">
    <DsfrBreadcrumb :links="breadcrumbLinks" />
    <h1 class="fr-h4 mb-0">{{ pageTitle }}</h1>
    <div class="filters mb-8">
      <slot name="primary"></slot>
    </div>
    <!-- could make choice of box/accordion a prop, then for views up to md always use accordion to save space -->
    <DsfrAccordionsGroup v-if="$slots.accordion" v-model="activeAccordion" class="border mb-8 filter-area">
      <DsfrAccordion id="filter-accordeon" title="Filtres">
        <template v-slot:title>
          <h2 class="fr-accordion__title">
            <v-icon name="ri-equalizer-fill"></v-icon>
            Filtres
          </h2>
        </template>
        <div class="p-2">
          <slot name="accordion"></slot>
        </div>
      </DsfrAccordion>
    </DsfrAccordionsGroup>
    <div class="mb-8" v-if="$slots['filter-box']">
      <h2 class="fr-text--lg mb-1">
        <v-icon name="ri-equalizer-fill"></v-icon>
        Filtres
      </h2>
      <div class="border p-4 filters">
        <slot name="filter-box"></slot>
      </div>
    </div>
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="data && data.count > 0">
      <div class="text-right">
        <p class="text-sm! -mb-2 -mt-4 font-medium" aria-live="polite">
          {{ data.count }} {{ data.count === 1 ? "résultat" : "résultats" }}
        </p>
      </div>
      <div class="overflow-scroll">
        <slot name="table"></slot>
      </div>
      <DsfrPagination
        v-if="showPagination"
        @update:currentPage="(newPage) => $emit('updatePage', newPage)"
        :pages="pages"
        :current-page="page - 1"
        :truncLimit="5"
      />
    </div>
    <div v-else class="h-40 sm:h-60 rounded bg-slate-100 mb-8 flex flex-col items-center content-center justify-center">
      <slot name="no-results" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { getPagesForPagination } from "@/utils/components"
import { setDocumentTitle } from "@/utils/document"
import ProgressSpinner from "@/components/ProgressSpinner"

const props = defineProps({ breadcrumbLinks: Array, data: Object, isFetching: Boolean, limit: String, route: Object })

const activeAccordion = ref()

const page = computed(() => parseInt(props.route?.query.page))
const pages = computed(() => getPagesForPagination(props.data?.count, props.limit, props.route?.path))
const showPagination = computed(() => props.data?.count > props.data?.results?.length)

const pageTitle = computed(() => props.breadcrumbLinks[props.breadcrumbLinks.length - 1].text)

const updateDocumentTitle = () => {
  setDocumentTitle([pageTitle.value], {
    number: page.value,
    total: pages.value.length,
    term: "page",
  })
}
watch(page, async () => {
  updateDocumentTitle()
})
watch(pages, async () => {
  updateDocumentTitle()
})
</script>

<style scoped>
@reference "../styles/index.css";

/* le bouton de l'accordéon devrait être en bleu,
mais la couleur de l'h2 prend précedence sans ce CSS */
h2.fr-accordion__title {
  color: unset;
}

.filters :deep(.fr-input-group) {
  @apply my-0;
}
.filters :deep(.fr-select-group) {
  @apply mb-0;
}
</style>
