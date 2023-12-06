<template>
  <div class="bg-slate-100">
    <div class="fr-container p-6 py-6 sm:py-10 md:py-16 grid grid-cols-12">
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
          <router-link :to="{ name: 'LandingPage' }">Eucalyptus</router-link>
          ,
          <router-link :to="{ name: 'LandingPage' }">Carotte</router-link>
          ,
          <router-link :to="{ name: 'LandingPage' }">Vitamine B12</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"

const searchTerm = ref(null)

const search = () => {
  console.log(`Effectuer recherche avec ${searchTerm.value}`)
}
</script>
