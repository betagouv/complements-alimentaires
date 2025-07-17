<template>
  <HistorySection v-if="snapshots" :snapshots="snapshots" :hideInstructionDetails="true" />
  <div v-else>
    <SectionHeader icon="ri-history-fill" text="Historique non disponible" />
    <p>L'historique est seulement accessible pour les déclarations refusées ou abandonnées.</p>
  </div>
</template>

<script setup>
import HistorySection from "@/components/NewBepiasViews/HistorySection"
import SectionHeader from "@/components/NewBepiasViews/SectionHeader"
defineProps({ snapshots: Array })
</script>
