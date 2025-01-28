<template>
  <div class="bg-blue-france-975 relative">
    <img class="hidden lg:block absolute scale-75 top-32 left-1" src="/static/images/cloud-left.png" />
    <img class="hidden md:block absolute scale-75 top-5 right-1" src="/static/images/cloud-right.png" />
    <img class="hidden md:block absolute bottom-0 right-20" src="/static/images/plants.png" />
    <div class="relative fr-container py-6 sm:py-10 md:py-16 grid grid-cols-12">
      <div class="col-span-12 md:col-span-8 lg:col-span-6">
        <h1>Vers une circulation de compléments alimentaires sûrs et conformes</h1>
        <router-link :to="{ name: 'BlogHomePage' }" class="fr-btn fr-btn--md mt-4">
          En savoir plus sur la réglementation
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup></script>
