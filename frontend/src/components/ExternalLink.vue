<template>
  <a :href="href" target="_blank" rel="noopener external" :title="`${text || href} - nouvelle fenêtre`" class="fr-link">
    <!-- ici on mets le texte dans un span pour éviter un espace additionel entre le texte et l'icône -->
    <!-- qui est introduit avec le texte en sr-only. Le &nbsp; assure que l'espace est introduit au début du text sr-only. -->
    <span>{{ text || href }}</span>
    <span class="fr-sr-only">&nbsp;- nouvelle fenêtre</span>
  </a>
</template>

<script setup>
defineProps({ href: String, text: String })
</script>
