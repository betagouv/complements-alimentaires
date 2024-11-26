<template>
  <div>
    <ElementAutocomplete
      autocomplete="nothing"
      label="Chercher un ingrédient dans la base de données"
      label-visible
      hint="Tapez au moins trois caractères pour démarrer la recherche"
      @selected="selectOption"
      :hideSearchButton="true"
      :optional="true"
    />
    <div class="mt-4" v-if="selectedOption">
      <ResultCard :result="selectedOption" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import ElementAutocomplete from "@/components/ElementAutocomplete.vue"
import ResultCard from "./ResultCard.vue"

const emit = defineEmits(["replacement-id"])

const selectedOption = ref()

const selectOption = (option) => {
  selectedOption.value = option
  emit("replacement-id", option.id)
}
</script>
