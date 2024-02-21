<template>
  <h2 class="fr-h6">
    <v-icon class="mr-1" name="ri-flask-line" />
    Ingrédients
  </h2>

  <ElementAutocomplete
    v-model="searchTerm"
    :options="autocompleteResults"
    autocomplete="nothing"
    label="Cherchez un ingrédient"
    label-visible
    class="max-w-md"
    hint="Tapez au moins trois caractères pour démarrer la recherche"
    @selected="selectOption"
  />

  <div v-if="chosenIngredients && chosenIngredients.length" class="mt-4">
    <div v-for="ingredient in chosenIngredients" :key="ingredient.id" class="p-4 border">
      <v-icon scale="0.85" class="mr-2" :name="getTypeIcon(ingredient.objectType)" />
      {{ ingredient.name }}
    </div>
  </div>
  <div v-else class="my-12">
    <v-icon name="ri-information-line" class="mr-1"></v-icon>
    Vous n'avez pas encore saisi d'ingrédients pour votre complément alimentaire
  </div>
</template>

<script setup>
import { ref, watch } from "vue"
import { useFetch } from "@vueuse/core"
import { headers, getTypeIcon } from "@/utils"
import ElementAutocomplete from "@/components/ElementAutocomplete.vue"

const autocompleteResults = ref([])
const searchTerm = ref("")
const chosenIngredients = ref([])

const onAutocompleteChange = () => {
  if (searchTerm.value.length < 3) {
    autocompleteResults.value = []
    return
  }
  return fetchSearchResults()
}

const selectOption = (result) => {
  chosenIngredients.value.push(result)
  searchTerm.value = ""
  autocompleteResults.value = []
}

const fetchSearchResults = async () => {
  const body = { term: searchTerm.value }
  const { error, data } = await useFetch("/api/v1/substances/autocomplete/", { headers }).post(body).json()

  if (error.value) {
    window.alert("Une erreur est survenue veuillez réessayer plus tard")
    console.error(error.value)
    return
  }
  autocompleteResults.value = data.value
}

watch(searchTerm, onAutocompleteChange)
</script>
