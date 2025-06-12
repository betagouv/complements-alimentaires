<template>
  <div>
    <div v-if="snapshot">
      <div class="p-4 bg-white rounded mb-4">
        <SnapshotItem :snapshot="snapshot" />
      </div>

      <DsfrButton @click="goToHistory" label="Voir l'historique" secondary size="small" />
    </div>
    <p v-else>Aucun commentaire n'a été ajouté</p>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router"
import SnapshotItem from "@/components/SnapshotItem"

const route = useRoute()
const router = useRouter()
defineProps({ snapshot: Object })

const goToHistory = () => router.push({ name: "HistorySection", params: route.params })
</script>
