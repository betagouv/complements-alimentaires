<template>
  <h2 class="fr-h6">
    <v-icon class="mr-1" name="ri-flask-line" />
    Ingrédients
  </h2>

  <DsfrInputGroup class="max-w-md">
    <DsfrInput
      @keydown="onAutocompleteChange"
      v-model="searchTerm"
      label="Cherchez un ingrédient"
      hint="Tapez au moins trois caractères pour démarrer la recherche"
      label-visible
    />
    <div v-if="autocompleteResults.length > 0" class="absolute left-2 min-w-80 border rounded-sm z-10">
      <button class="min-w-full" v-for="result in autocompleteResults" :key="result.id" @click="selectOption(result)">
        <div class="p-2 bg-white hover:bg-blue-france-975 text-left flex">
          <div class="self-center"><v-icon scale="0.85" class="mr-2" :name="getTypeIcon(result.objectType)" /></div>
          <div>
            <div class="font-bold">{{ result.name }}</div>
            <div>{{ getType(result.objectType) }}</div>
          </div>
        </div>
      </button>
    </div>
  </DsfrInputGroup>
  <div v-if="chosenIngredients && chosenIngredients.length">
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
import { ref } from "vue"
import { headers, verifyResponse, getTypeIcon } from "@/utils"

const autocompleteResults = ref([])
const loading = ref(false)
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

// TODO : Should use a specific API for autocomplete
const fetchSearchResults = () => {
  const url = "/api/v1/search/"
  const body = JSON.stringify({ search: searchTerm.value, limit: 6, offset: 0 })
  loading.value = true
  return fetch(url, { method: "POST", headers, body })
    .then(verifyResponse)
    .then((response) => (autocompleteResults.value = response.results))
    .catch((e) => {
      window.alert("Une erreur est survenue veuillez réessayer plus tard")
      console.error(e)
    })
    .finally(() => (loading.value = false))
}

const getType = (objectType) => {
  const mapping = {
    plant: "Plante",
    microorganism: "Micro-organisme",
    ingredient: "Ingredient",
    substance: "Substance",
  }
  return mapping[objectType] || null
}
</script>
