<template>
  <div class="bg-grey-975! p-6" v-if="snapshots">
    <SectionHeader icon="ri-history-fill" text="Historique" />

    <div v-if="!snapshots" class="flex justify-center items-center min-h-60">
      <ProgressSpinner />
    </div>
    <div v-if="snapshots.length" class="flex flex-col gap-6">
      <SnapshotItem
        v-for="snapshot in snapshots"
        :key="`snapshot-${snapshot.id}`"
        :snapshot="snapshot"
        :rightSide="showOnRight(snapshot)"
      />
    </div>
    <div v-else>
      <p>Nous n'avons pas l'historique pour cette déclaration.</p>
    </div>
  </div>
</template>

<script setup>
import ProgressSpinner from "@/components/ProgressSpinner"
import SnapshotItem from "@/components/SnapshotItem"
import SectionHeader from "../SectionHeader"

defineProps({ snapshots: Array })

const showOnRight = (snapshot) => {
  const rightSideStatus = ["OBSERVATION", "AUTHORIZED", "ONGOING_INSTRUCTION", "AWAITING_VISA", "OBJECTION", "REJECTED"]
  return rightSideStatus.indexOf(snapshot.status) > -1
}
</script>
