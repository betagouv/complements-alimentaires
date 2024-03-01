<template>
  <div class="bg-blue-france-975 relative">
    <img class="hidden lg:block absolute scale-75 top-32 left-1" src="/static/images/cloud-left.png" />
    <img class="hidden md:block absolute scale-75 top-5 right-1" src="/static/images/cloud-right.png" />
    <img class="hidden md:block absolute bottom-0 right-20" src="/static/images/plants.png" />
    <div class="fr-container relative p-6 py-6 sm:py-10 md:py-14 grid grid-cols-12">
      <div class="col-span-12 md:col-span-8 lg:col-span-5">
        <h1>Tester ma composition de compléments alimentaires</h1>
        <p>Vérifier la conformité de vos ingrédients en amont de vos développements produits.</p>
        <DsfrSearchBar
          placeholder="Rechercher par ingrédient, plante, substance..."
          v-model="searchTerm"
          @search="search"
        />
        <p class="mt-6">
          Examples :
          <router-link :to="getRouteForTerm('Eucalyptus')">Eucalyptus</router-link>
          ,
          <router-link :to="getRouteForTerm('Carotte')">Carotte</router-link>
          ,
          <router-link :to="getRouteForTerm('Vitamine B12')">Vitamine B12</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"

const searchTerm = ref(null)
const router = useRouter()

const search = () => {
  if (searchTerm.value.length < 3) window.alert("Veuillez saisir au moins trois caractères")
  else router.push(getRouteForTerm(searchTerm.value))
}
const getRouteForTerm = (term) => {
  return { name: "SearchResultsPage", query: { q: term } }
}
</script>
