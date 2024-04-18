<template>
  <SectionTitle title="Nouveaux ingrédients" sizeTag="h6" icon="ri-flask-line" />
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
import SectionTitle from "@/components/SectionTitle"

const payload = defineModel()

const newPlants = computed(() => payload.value.declaredPlants.filter((x) => x.new))
const newMicroorganisms = computed(() => payload.value.declaredMicroorganisms.filter((x) => x.new))
const newIngredients = computed(() => payload.value.declaredIngredients.filter((x) => x.new))
</script>
