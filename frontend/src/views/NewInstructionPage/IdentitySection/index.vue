<template>
  <div>
    <div class="bg-grey-975! p-6">
      <h2 id="declarant-e">Déclarant·e</h2>
      <DsfrAlert small description="Ce segment est en construction" class="mb-6" />
      <h2 id="produit">Informations sur le produit</h2>
      <DsfrAlert small description="Ce segment est en construction" class="mb-6" />
      <h2 id="entreprise">Identité de l’entreprise</h2>
      <DsfrAlert small description="Ce segment est en construction" class="mb-6" />
    </div>
  </div>
</template>

<script setup>
defineProps({ declarant: Object, company: Object })
</script>
