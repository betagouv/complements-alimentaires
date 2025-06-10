<template>
  <div>
    <div class="bg-grey-975! p-6">
      <h2 id="pieces-jointes">Pièces jointes</h2>
      <CompactAttachmentGrid :attachments="declaration.attachments" />
      <h2 id="dernier-commentaire">Dernier commentaire</h2>
      <DsfrAlert small description="Ce segment est en construction" class="mb-6" />
      <h2 id="composition-produit">Composition produit</h2>
      <DsfrAlert small description="Ce segment est en construction" class="mb-6" />
      <h2 id="resultat-instruction">Résultat de l'instruction</h2>
      <DsfrAlert small description="Ce segment est en construction" class="mb-6" />
      <h3 id="decision">Décision</h3>
      <DsfrAlert small description="Ce segment est en construction" class="mb-6" />
      <h3 id="justification">Justification de la contestation</h3>
      <DsfrAlert small description="Ce segment est en construction" class="mb-6" />
    </div>
    <div class="p-6">
      <h2 id="notes">Notes à destination de l'administration</h2>
      <DsfrAlert small description="Ce segment est en construction" class="mb-6" />
    </div>
  </div>
</template>

<script setup>
import CompactAttachmentGrid from "@/components/CompactAttachmentGrid.vue"

defineProps({ declaration: Object })
</script>
