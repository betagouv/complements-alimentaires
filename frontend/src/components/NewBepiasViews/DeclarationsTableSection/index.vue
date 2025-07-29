<template>
  <div>
    <DsfrAccordionsGroup v-model="activeAccordion" class="mb-8">
      <DsfrAccordion title="Filtrer les déclarations">
        <div class="grid grid-cols-3">
          <div class="col-span-1 sm:col-span-2 md:col-span-3">
            <DsfrToggleSwitch
              label="Afficher les déclarations à surveiller uniquement"
              :modelValue="surveillanceOnly"
              @update:modelValue="updateSurveillanceOnly"
            />
          </div>
        </div>
      </DsfrAccordion>
    </DsfrAccordionsGroup>
    <div v-if="isFetching && !data" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else>
      <ControlDeclarationsTable :data="data" v-if="data" @sort="updateOrdering" @filter="updateFiltering" />
      <DsfrPagination
        v-if="showPagination"
        @update:currentPage="updatePage"
        :pages="pages"
        :current-page="page - 1"
        :truncLimit="5"
      />
    </div>
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { computed, watch } from "vue"
import { getPagesForPagination } from "@/utils/components"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import ControlDeclarationsTable from "./ControlDeclarationsTable"
import { ref } from "vue"

const activeAccordion = ref()

const props = defineProps({ companyId: String })

const router = useRouter()
const route = useRoute()

const offset = computed(() => (page.value - 1) * limit.value)
const pages = computed(() => getPagesForPagination(data.value?.count, limit.value, route.path))

const page = computed(() => parseInt(route.query.page))
const ordering = computed(() => route.query.triage)
const limit = computed(() => parseInt(route.query.limit))
const simplifiedStatus = computed(() => route.query.simplifiedStatus)
const surveillanceOnly = computed(() => route.query.surveillanceOnly === "true")

const showPagination = computed(() => data.value?.count > data.value?.results?.length)

// Obtention de la donnée via API
const url = computed(() => {
  const apiUrl = `/api/v1/control/declarations/?limit=${limit.value}&offset=${offset.value}&ordering=${ordering.value}&simplifiedStatus=${simplifiedStatus.value}&surveillanceOnly=${surveillanceOnly.value}`
  if (props.companyId) return `${apiUrl}&company=${props.companyId}`
  return apiUrl
})
const { response, data, isFetching, execute } = useFetch(url).get().json()

const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

// Mise à jour des paramètres
const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...{ page: 1 }, ...newQuery } })
const updateSurveillanceOnly = (value) => updateQuery({ surveillanceOnly: value ? "true" : "false" })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateOrdering = (sortValue) => updateQuery({ triage: sortValue || "-creationDate" })
const updateFiltering = (filterKey, filterValue) => {
  const filterQuery = {}
  filterQuery[filterKey] = filterValue
  updateQuery(filterQuery)
}

watch([page, limit, ordering, simplifiedStatus, surveillanceOnly], fetchSearchResults)
</script>
