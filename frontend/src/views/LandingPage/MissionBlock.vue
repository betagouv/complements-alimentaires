<template>
  <div class="fr-container p-6 sm:py-4! sm:px-0! grid grid-cols-12 gap-0 sm:gap-4 md:gap-10">
    <div class="col-span-12 md:col-span-6">
      <h2>Notre Mission</h2>
      <p class="fr-h6">Accroître la transparence du secteur des compléments alimentaires</p>
      <p class="fr-text--alt italic">Car aujourd’hui, 60% des français en consomment régulièrement.</p>
    </div>
    <div class="col-span-12 md:col-span-6">
      <h3 class="fr-h6">Concrètement, notre service a vocation :</h3>
      <ul class="list-none">
        <li class="flex" v-for="point in bulletPoints" :key="point.text">
          <div class="mr-3 text-xl">{{ point.icon }}</div>
          <p class="mb-2!">{{ point.text }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
const bulletPoints = [
  {
    icon: "🗂️",
    text: "Faciliter et fluidifier l’instruction des mises sur le marché de compléments alimentaires",
  },
  {
    icon: "🤝",
    text: "Autonomiser et responsabiliser les professionnels du secteur en leur fournissant les ressources et outils",
  },
  {
    icon: "🤔",
    text: "Informer les consommateurs, les rendre acteurs de leur consommation",
  },
]
</script>
