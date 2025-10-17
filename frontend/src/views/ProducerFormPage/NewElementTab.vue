<template>
  <div>
    <SectionTitle title="Nouveaux ingrédients" sizeTag="h6" icon="ri-flask-line" />
    <p>
      Vous avez ajouté de nouveaux ingrédients ou nouvelles parties de plantes. Des informations complémentaires sont
      requises.
    </p>
    <NewElementList objectType="plant" :elements="newPlants" />
    <NewElementList objectType="plant_part" :elements="newPlantParts" />
    <NewElementList objectType="microorganism" :elements="newMicroorganisms" />
    <NewElementList objectType="form_of_supply" :elements="getObjectSubTypeList(newIngredients, 'form_of_supply')" />
    <NewElementList objectType="aroma" :elements="getObjectSubTypeList(newIngredients, 'aroma')" />
    <NewElementList objectType="additive" :elements="getObjectSubTypeList(newIngredients, 'additive')" />
    <NewElementList
      objectType="active_ingredient"
      :elements="getObjectSubTypeList(newIngredients, 'active_ingredient')"
    />
    <NewElementList
      objectType="non_active_ingredient"
      :elements="getObjectSubTypeList(newIngredients, 'non_active_ingredient')"
    />

    <NewElementList objectType="substance" :elements="newSubstances" />
  </div>
</template>

<script setup>
import { computed } from "vue"
import NewElementList from "./NewElementList"
import SectionTitle from "@/components/SectionTitle"
import { getObjectSubTypeList } from "@/utils/elements"

const payload = defineModel()

const newPlants = computed(() => payload.value.declaredPlants.filter((x) => x.new))
const newPlantParts = computed(() =>
  payload.value.declaredPlants.filter(
    (x) => !x.new && x.usedPart && x.element?.plantParts?.find((ep) => ep.id === x.usedPart)?.status !== "autorisé"
  )
)
const newMicroorganisms = computed(() => payload.value.declaredMicroorganisms.filter((x) => x.new))
const newIngredients = computed(() => payload.value.declaredIngredients.filter((x) => x.new))
const newSubstances = computed(() => payload.value.declaredSubstances.filter((x) => x.new))
</script>
