<template>
  <div class="grid grid-cols-12">
    <div class="col-span-12 md:col-span-8 lg:col-span-6">
      <h3 class="mb-1">Vous êtes un•e professionnel•le du secteur et souhaitez déclarer un produit ?</h3>
      <p class="my-4">Suivez notre checklist pour vous orienter vers la bonne démarche de déclaration.</p>
      <DsfrButton label="Préparer ma télédéclaration" @click="$router.push({ name: 'NewDeclaration' })" />
    </div>
    <div class="hidden md:flex md:col-span-4 lg:col-span-6 justify-center content-center">
      <img
        style="max-width: 90%; max-height: 90%; object-fit: contain"
        src="/static/images/illustrations/declaration-illustration.png"
        alt="Professionnelle effectuant sa déclaration"
      />
    </div>
  </div>
</template>

<script setup></script>
