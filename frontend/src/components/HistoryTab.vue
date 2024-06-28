<template>
  <div>
    <div v-if="isFetching" class="flex justify-center items-center min-h-60">
      <ProgressSpinner />
    </div>
    <div v-if="snapshots && snapshots.length" class="flex flex-col gap-6">
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
import { useFetch } from "@vueuse/core"
import { onMounted } from "vue"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import SnapshotItem from "@/components/SnapshotItem"

const props = defineProps(["declarationId"])

const {
  response,
  data: snapshots,
  execute,
  isFetching,
} = useFetch(() => `/api/v1/declarations/${props.declarationId}/snapshots/`, { immediate: false })
  .get()
  .json()

onMounted(async () => {
  await execute()
  handleError(response)
})

const showOnRight = (snapshot) => {
  const rightSideStatus = ["OBSERVATION", "AUTHORIZED", "AWAITING_VISA"]
  return rightSideStatus.indexOf(snapshot.status) > -1
}
</script>
