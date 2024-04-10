<template>
  <h2 class="fr-h6">
    <v-icon class="mr-1" name="ri-flask-line" />
    Nouveaux ingrédients
  </h2>
  <p>
    Vous avez ajouté les nouveaux ingrédients affichés ci-dessous. Des informations supplémentaires les concernant sont
    requises.
  </p>
  <NewElementList objectType="plant" :elements="newPlants" />
  <NewElementList objectType="microorganism" :elements="newMicroorganisms" />
  <NewElementList objectType="ingredient" :elements="newIngredients" />
</template>

<script setup>
import { computed } from "vue"
import NewElementList from "./NewElementList"
const payload = defineModel()

const newPlants = computed(() => payload.value.declaredPlants.filter((x) => x.new))
const newMicroorganisms = computed(() => payload.value.declaredMicroorganisms.filter((x) => x.new))
const newIngredients = computed(() => payload.value.declaredIngredients.filter((x) => x.new))
</script>
