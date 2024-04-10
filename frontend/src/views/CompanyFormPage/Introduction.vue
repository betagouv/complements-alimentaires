<template>
  <div>Vous allez pouvoir créer une nouvelle entreprise ou en rejoindre une existante.</div>
  <div>
    Vous pourrez à tout moment revenir en arrière et corriger les informations entrées avant validation définitive.
  </div>

  <!-- <DsfrAlert class="mt-4" type="warning">
    <strong>Ne fermez pas votre navigateur</strong>
    jusqu'à la validation de la dernière étape, sinon vous perdrez les données entrées.
  </DsfrAlert> -->
  <div class="mt-4">
    <DsfrButton @click="$emit('changeStep')" label="Démarrer" size="lg" />
  </div>
</template>

<script setup>
defineEmits(["changeStep"])
</script>
