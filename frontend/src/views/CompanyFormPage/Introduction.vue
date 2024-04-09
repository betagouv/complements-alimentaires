<template>
  <h1>Créer ou rejoindre une entreprise</h1>
  <div>Vous allez pouvoir créer une nouvelle entreprise ou en rejoindre une existante.</div>
  <div>
    Vous pourrez à tout moment revenir en arrière et corriger les informations entrées avant validation définitive.
  </div>

  <DsfrAlert class="mt-4" type="warning">
    <strong>Ne fermez pas votre navigateur</strong>
    jusqu'à la validation de la dernière étape, sinon vous perdrez les données entrées.
  </DsfrAlert>
  <div class="mt-4 mx-auto">
    <DsfrButton @click="$emit('nextStep')" label="Démarrer" size="lg" />
  </div>
</template>

<script setup>
defineEmits(["nextStep"])
</script>
