<template>
  <div class="fr-container pb-8">
    <DsfrBreadcrumb
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Recherche entreprises' }]"
    />
    <h1 class="fr-h3">Entreprises responsables de la mise sur le marché</h1>

    <div class="md:flex justify-between">
      <div class="md:w-1/3 lg:w-2/5 pt-1">
        <DsfrFieldset>
          <DsfrSearchBar
            v-model="searchTerm"
            label="Nom de l'entreprise, No. SIRET, ou No. de TVA"
            placeholder="Nom de l'entreprise, No. SIRET, ou No. de TVA"
            @search="search"
            @update:modelValue="(val) => val === '' && search()"
          />
        </DsfrFieldset>
      </div>
      <div class="mb-4 md:mb-0" v-if="data?.results?.length && data?.results?.length <= MAX_EXPORT_RESULTS">
        <a :href="excelUrl" download class="bg-none">
          <DsfrButton label="Télécharger" secondary size="sm" icon="ri-file-excel-2-fill"></DsfrButton>
        </a>
      </div>
      <div class="mb-4 md:mb-0" v-if="data?.results?.length && data?.results?.length > MAX_EXPORT_RESULTS">
        <DsfrButton
          secondary
          size="sm"
          icon="ri-file-excel-2-fill"
          label="Télécharger"
          @click="exportModalOpened = true"
        />
        <PaginatedExcelDownload
          v-model="exportModalOpened"
          :baseUrl="excelUrl"
          :maxLines="MAX_EXPORT_RESULTS"
          :totalLines="data.count"
        />
      </div>
    </div>

    <!-- Zone des filtres actifs -->
    <div class="mb-4">
      <DsfrTag
        v-for="(item, idx) in activeFilters"
        :key="`active-filters-${idx}`"
        :label="item.text"
        tagName="button"
        @click="item.callback"
        :aria-label="`Retirer le filtre « ${item.text} »`"
        class="mx-1 fr-tag--dismiss"
      ></DsfrTag>
    </div>

    <div class="grid grid-cols-4 gap-4 mb-6">
      <div class="col-span-4 md:col-span-2 lg:col-span-1">
        <DsfrMultiselect
          label="Département de l'entreprise"
          hint="Le département de domiciliation du siège"
          v-model="departments"
          :options="departmentOptions()"
          :search="true"
        />
      </div>
      <div class="col-span-4 md:col-span-2 lg:col-span-1">
        <DsfrMultiselect
          label="Rôle de l'entreprise"
          hint="Fabricant, importateur, distributeur, etc."
          v-model="roles"
          :options="roleOptions()"
          :search="true"
        />
      </div>
    </div>

    <div v-if="isFetching && !data" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="data?.results?.length">
      <ControlCompanyTable :data="data" @sort="updateOrdering" />
      <DsfrPagination
        v-if="showPagination"
        @update:currentPage="updatePage"
        :pages="pages"
        :current-page="page - 1"
        :truncLimit="5"
      />
    </div>
    <div v-else class="border p-4 rounded mb-4 bg-gray-50">
      <p class="mb-0">Aucune entreprise trouvée avec les paramètres spécifiés</p>
    </div>
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { computed, watch, ref } from "vue"
import { getPagesForPagination } from "@/utils/components"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import ControlCompanyTable from "./ControlCompanyTable"
import jsonDepartments from "@/utils/departments.json"
import { allActivities } from "@/utils/mappings"
import PaginatedExcelDownload from "@/components/PaginatedExcelDownload"

const MAX_EXPORT_RESULTS = 2000

const exportModalOpened = ref(false)

const router = useRouter()
const route = useRoute()

const offset = computed(() => (page.value - 1) * limit.value)
const pages = computed(() => getPagesForPagination(data.value?.count, limit.value, route.path))

const page = computed(() => parseInt(route.query.page))
const ordering = computed(() => route.query.triage)
const limit = computed(() => parseInt(route.query.limit))
const showPagination = computed(() => data.value?.count > data.value?.results?.length)

const searchTerm = ref(route.query.recherche)
const departments = ref(route.query.departments?.split(",").filter((x) => !!x) || [])
const roles = ref(route.query.roles?.split(",").filter((x) => !!x) || [])

const departmentOptions = () => {
  const departments = jsonDepartments.map((x) => `${x.departmentCode} - ${x.departmentName}`)
  departments.push("99 - Étranger")
  return departments
}

const roleOptions = () => allActivities.map((x) => x.label)

// Obtention de la donnée via API
const commonApiParams = computed(() => {
  let apiParams = `ordering=${ordering.value}`
  if (searchTerm.value) apiParams += `&search=${searchTerm.value}`
  if (departments.value.length) apiParams += `&departments=${departments.value.map((x) => x.split(" - ")[0]).join(",")}`
  if (roles.value.length)
    apiParams += `&activities=${roles.value.map((x) => allActivities.find((y) => y.label === x).value).join(",")}`
  return apiParams
})
const url = computed(
  () => `/api/v1/control/companies/?limit=${limit.value}&offset=${offset.value}&${commonApiParams.value}`
)
const { response, data, isFetching, execute } = useFetch(url).get().json()

const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

// Export Excel

const excelUrl = computed(() => `/api/v1/control/companies-export.xlsx?${commonApiParams.value}`)

// Mise à jour des paramètres
const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...{ page: 1 }, ...newQuery } })

const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateOrdering = (sortValue) => updateQuery({ triage: sortValue || "-creationDate" })

const search = () => updateQuery({ recherche: searchTerm.value })

watch(route, fetchSearchResults)
watch(departments, () => updateQuery({ departments: departments.value.join(",") }))
watch(roles, () => updateQuery({ roles: roles.value.join(",") }))

// Filter tags

const activeFilters = computed(() => {
  const filters = []
  if (departments.value?.length)
    for (let i = 0; i < departments.value.length; i++) {
      const department = departments.value[i]
      filters.push({
        text: department,
        callback: () => (departments.value = departments.value.filter((x) => x !== department)),
      })
    }

  if (roles.value?.length)
    for (let i = 0; i < roles.value.length; i++) {
      const role = roles.value[i]
      filters.push({
        text: role,
        callback: () => (roles.value = roles.value.filter((x) => x !== role)),
      })
    }
  return filters
})
</script>
