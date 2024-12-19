<template>
  <div>
    <p>{{ company || "Inconnue" }}</p>
    <p v-if="mandatedCompany" class="italic text-sm">Représentée par {{ mandatedCompany }}</p>
  </div>
</template>

<script setup>
defineProps({ company: String, mandatedCompany: String })
</script>
