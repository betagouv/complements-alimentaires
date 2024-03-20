<template>
  <h2 class="fr-h6">
    <v-icon class="mr-1" name="ri-flask-line" />
    Nouveaux ingrédients
  </h2>
  <p>
    Vous avez ajoté les nouveaux ingrédients affichés ci-dessous. Des informations supplémentaires les concernant sont
    requises.
  </p>
  <div>
    <NewElementCard :key="index" v-for="(element, index) in newElements" v-model="newElements[index]" />
  </div>
</template>

<script setup>
import { computed } from "vue"
import NewElementCard from "./NewElementCard"
const payload = defineModel()

const newElements = computed(() => payload.value.elements.filter((x) => x.element.new))
</script>
