<template>
  <div class="fr-container py-8">
    <DsfrErrorPage
      title="Page non trouvée"
      subtitle="Erreur 404"
      description="La page que vous cherchez n’existe pas ou l’url est erronée."
      class="!p-0"
    />
    <router-link :to="{ name: 'BlogsHome' }" class="fr-btn fr-btn--md mt-0 mb-8">Page d'accueil</router-link>
  </div>
</template>
