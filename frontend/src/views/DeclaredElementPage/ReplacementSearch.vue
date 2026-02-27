<template>
  <div>
    <ElementAutocomplete
      label="Chercher un ingrédient dans la base de données"
      label-visible
      hint="Tapez au moins trois caractères pour démarrer la recherche"
      @selected="selectOption"
      :required="false"
    />
    <div class="mt-4" v-if="selectedOption">
      <ResultCard :result="selectedOption" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { getApiType } from "@/utils/mappings"
import ElementAutocomplete from "@/components/ElementAutocomplete.vue"
import ResultCard from "./ResultCard.vue"

const emit = defineEmits(["replacement-id"])

const selectedOption = ref()

const selectOption = (option) => {
  selectedOption.value = option // quick and temporary display
  emit("replacement", option)
  fetchElement(getApiType(option.objectType), option.objectType, option.id).then((item) => {
    selectedOption.value = item
    emit("replacement", item)
  })
  // TODO: erase search term from search bar?
}

// TODO: turn into service ? It was taken from another file
const fetchElement = async (apiType, type, id) => {
  const { data, response } = await useFetch(`/api/v1/${apiType}s/${id}`).get().json()
  await handleError(response)
  if (!response.value.ok) return null
  return { ...data.value, ...{ objectType: type } }
}
</script>
