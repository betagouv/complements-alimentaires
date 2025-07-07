<template>
  <div class="bg-blue-france-975 relative">
    <img class="hidden lg:block absolute scale-75 top-32 left-1" src="/static/images/cloud-left.png" alt="" />
    <img class="hidden md:block absolute scale-75 top-5 right-1" src="/static/images/cloud-right.png" alt="" />
    <img class="hidden md:block absolute bottom-0 right-20" src="/static/images/plants.png" alt="" />
    <div class="fr-container relative p-6 py-6 sm:py-10 md:py-14 grid grid-cols-12">
      <div class="col-span-12 md:col-span-8 lg:col-span-5">
        <h1>Tester ma composition de compléments alimentaires</h1>
        <p>Vérifier la conformité de vos ingrédients en amont de vos développements produits.</p>
        <ElementAutocomplete
          autocomplete="nothing"
          class="max-w-md grow"
          label="Cherchez un ingrédient"
          hint="Tapez au moins trois caractères pour démarrer la recherche"
          @selected="goToSelectedOption"
          @search="search"
          :chooseFirstAsDefault="false"
        />
        <p class="mt-6">
          Exemples :
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
import { useRouter } from "vue-router"
import { slugifyType } from "@/utils/mappings"
import ElementAutocomplete from "@/components/ElementAutocomplete.vue"

const router = useRouter()

const search = (term) => {
  if (term.length < 3) window.alert("Veuillez saisir au moins trois caractères")
  else router.push(getRouteForTerm(term))
}
const getRouteForTerm = (term) => {
  return { name: "ElementSearchResultsPage", query: { q: term } }
}
const goToSelectedOption = (option) => {
  const slugguedType = slugifyType(option.objectType)
  const urlComponent = `${option?.id}--${slugguedType}--${option?.name}`
  return router.push({ name: "ElementPage", params: { urlComponent } })
}
</script>
