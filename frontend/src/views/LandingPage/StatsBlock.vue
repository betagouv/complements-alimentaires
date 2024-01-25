<template>
  <div class="bg-blue-france-975">
    <div class="fr-container p-6 py-6 sm:py-10 md:py-16 grid grid-cols-12 gap-0 md:gap-16">
      <div class="col-span-12 md:col-span-4" v-for="stat in stats" :key="stat.label">
        <div class="fr-text--alt text-5xl italic font-normal m-0 mb-4">{{ stat.number }}</div>
        <div class="fr-text--alt italic">{{ stat.label }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
const stats = [
  {
    number: "1600",
    label: "nouvelles déclarations de mises sur le marché tous les mois",
  },
  {
    number: "3",
    label: "instructrices pour couvrir l’ensemble de ces demandes",
  },
  {
    number: "50%",
    label: "de produits circulant dans la distribution mais non déclarés",
  },
]
</script>
