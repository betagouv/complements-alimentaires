<template>
  <div>
    <div>Vous allez pouvoir créer une nouvelle entreprise ou en rejoindre une existante.</div>
    <div>
      Vous pourrez à tout moment revenir en arrière et corriger les informations entrées avant validation définitive.
    </div>

    <div class="mt-4">
      <DsfrButton @click="$emit('changeStep')" label="Démarrer" size="lg" />
    </div>
  </div>
</template>

<script setup>
defineEmits(["changeStep"])
</script>
