<template>
  <div class="fr-container pb-8">
    <DsfrBreadcrumb
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Recherche entreprises' }]"
    />
    <h1 class="fr-h3">Entreprises responsables de la mise sur le marché</h1>

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
      <div class="col-span-4 md:col-span-2 lg:col-span-1">Filter rôle</div>
    </div>

    <div v-if="isFetching && !data" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else>
      <ControlCompanyTable :data="data" v-if="data" @sort="updateOrdering" />
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
import { computed, watch, ref } from "vue"
import { getPagesForPagination } from "@/utils/components"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import ControlCompanyTable from "./ControlCompanyTable"
import jsonDepartments from "@/utils/departments.json"

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

const departmentOptions = () => {
  const departments = jsonDepartments.map((x) => `${x.departmentCode} - ${x.departmentName}`)
  departments.push("99 - Étranger")
  return departments
}

// Obtention de la donnée via API
const url = computed(() => {
  let base = `/api/v1/control/companies/?limit=${limit.value}&offset=${offset.value}&ordering=${ordering.value}`
  if (searchTerm.value) base += `${base}&search=${searchTerm.value}`
  if (departments.value.length)
    base += `${base}&departments=${departments.value.map((x) => x.split(" - ")[0]).join(",")}`
  return base
})
const { response, data, isFetching, execute } = useFetch(url).get().json()

const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

// Mise à jour des paramètres
const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...{ page: 1 }, ...newQuery } })

const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateOrdering = (sortValue) => updateQuery({ triage: sortValue || "-creationDate" })

const search = () => updateQuery({ recherche: searchTerm.value })

watch(route, fetchSearchResults)
watch(departments, () => updateQuery({ departments: departments.value.join(",") }))
</script>
